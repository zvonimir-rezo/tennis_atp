"""Disposable temporal evaluation and sensitivity; reads existing verified features."""
import json,pickle
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.metrics import log_loss,brier_score_loss
from tennis_atp_pipeline.data import load_matches
m=load_matches(); d=pd.read_parquet('data/processed/model_training_rows.parquet'); d=d.query('a_pre_elo_matches_played>=20 and b_pre_elo_matches_played>=20')
with open('models/logreg_model.pkl','rb') as f:features=list(pickle.load(f).feature_names_in_)
tr=d[d.tourney_date_dt.dt.year<=2023];va=d[d.tourney_date_dt.dt.year==2024];te=d[(d.tourney_date_dt.dt.year==2025)&(d.player_a_id<d.player_b_id)].copy()
for name,fs in [('model',features),('rank',['log_rank_diff','diff_player_rank_points'])]:
 model=make_pipeline(SimpleImputer(),StandardScaler(),LogisticRegression(C=.1,max_iter=2000));model.fit(tr[fs],tr.player_a_wins)
 if name=='model':
  cal=CalibratedClassifierCV(FrozenEstimator(model),method='sigmoid');cal.fit(va[fs],va.player_a_wins);model=cal
 te[name]=model.predict_proba(te[fs])[:,1]
te=te.merge(m[['match_id','score','is_retirement']],on='match_id',suffixes=('','_source'));te['elo']=te.elo_expected_a
out={}
for label,sub in [('all',te),('completed',te[~te.score.str.contains('RET|W/O|DEF|ABD',na=False,regex=True)])]:
 out[label]={'matches':len(sub),'scores':{c:{'logloss':log_loss(sub.player_a_wins,sub[c]),'brier':brier_score_loss(sub.player_a_wins,sub[c])} for c in ['model','rank','elo']}}
# Paired tournament-date cluster bootstrap, a descriptive interval for this historical season.
y=te.player_a_wins.to_numpy(); eps=1e-15
for c in ['model','rank','elo']:
 p=np.clip(te[c].to_numpy(),eps,1-eps);te[c+'_loss']=-(y*np.log(p)+(1-y)*np.log(1-p))
rng=np.random.default_rng(20261021);blocks=[g for _,g in te.groupby('tourney_date_dt')];cis={}
for base in ['rank','elo']:
 draws=[]
 for _ in range(2000):
  chosen=rng.integers(len(blocks),size=len(blocks));total=sum(len(blocks[i]) for i in chosen)
  draws.append(sum((blocks[i][base+'_loss']-blocks[i].model_loss).sum() for i in chosen)/total)
 cis[base]={'mean_loss_improvement':float((te[base+'_loss']-te.model_loss).mean()),'cluster_bootstrap_95pct':np.quantile(draws,[.025,.975]).tolist()}
out['paired_comparison']=cis;out['caveat']='Retrospective diagnostic. Bootstrap resamples tournament-date groups, not independent seasons; model selection and previous inspection of 2025 are not accounted for.'
Path('reports/discovery/forecast-sensitivity.json').write_text(json.dumps(out,indent=2));te.to_parquet('reports/discovery/test-predictions.parquet',index=False);print(json.dumps(out,indent=2))
