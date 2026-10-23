"""Disposable discovery evidence. Run from repository root with PYTHONPATH=src:."""
import json, pickle, hashlib, sys, platform
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn, joblib
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.metrics import log_loss, brier_score_loss
from tennis_atp_pipeline.data import load_matches
from tennis_atp_pipeline.features import build_feature_tables

OUT=Path('reports/discovery'); OUT.mkdir(parents=True,exist_ok=True)
def dump(name,x):
 (OUT/name).write_text(json.dumps(x,indent=2,default=str))
 print(name,json.dumps(x,default=str)[:6500],flush=True)
m=load_matches(); d=pd.read_parquet('data/processed/model_training_rows.parquet')
dump('coverage.json',{'runtime':[platform.python_version(),pd.__version__,np.__version__,sklearn.__version__], 'matches':len(m),'unique_ids':m.match_id.nunique(),'players':len(set(m.winner_id)|set(m.loser_id)), 'by_year':m.groupby('source_year').size().to_dict(),'max_tournament_date':m.tourney_date_dt.max(),'ranking_dates':pd.read_csv('atp_rankings_current.csv').ranking_date.agg(['min','max']).to_dict(),'missing_percent':(100*m[['surface','minutes','w_svpt','l_svpt','winner_rank','loser_rank','winner_ht','loser_ht','winner_hand','loser_hand']].isna().mean()).round(3).to_dict(),'scores_special':m.score.str.extract('(RET|W/O|DEF|ABD)',expand=False).value_counts().to_dict(),'stored_training_rows':len(d),'training_dates':[d.tourney_date_dt.min(),d.tourney_date_dt.max()],'odds_raw_columns':pd.read_parquet('data/processed/odds_raw.parquet').columns.tolist()})
# Rebuild existing feature implementation in memory, keeping saved outputs untouched.
print('Rebuilding features in memory',flush=True)
t=build_feature_tables(m,write=False)
r=t['model_training_rows']; cols=[c for c in r if c in d]
merged=r.merge(d,on=['match_id','player_a_id'],suffixes=('_new','_saved'))
checks={}
for c in ['elo_expected_a','diff_pre_surface_elo','diff_pre_fatigue_index_v1','diff_pre_service_points_won_pct']:
 checks[c]={'equal':bool(np.allclose(merged[c+'_new'],merged[c+'_saved'],equal_nan=True)),'max_abs_diff':float((merged[c+'_new']-merged[c+'_saved']).abs().max())}
dump('rebuild.json',{'new_rows':len(r),'saved_rows':len(d),'joined_rows':len(merged),'checks':checks})
# Forecast evaluation: locked <=2023 fit, 2024 sigmoid calibration, 2025 report; mirror pairs stay in same year.
F=['diff_pre_surface_elo','diff_pre_overall_elo','elo_expected_a','diff_player_rank_points','diff_player_age','diff_pre_win_pct_last_10','diff_pre_surface_win_pct_last_10','diff_pre_h2h_decayed_net','diff_pre_service_points_won_pct','diff_pre_return_points_won_pct','diff_pre_win_after_winning_first_set_pct','diff_pre_win_after_losing_first_set_pct','diff_pre_fatigue_index_v1','diff_pre_days_since_last_match','diff_pre_matches_last_7_days','diff_pre_minutes_last_7_days','diff_pre_retirements_last_10_matches','a_is_lefty','b_is_lefty']
s=r.query('a_pre_elo_matches_played>=20 and b_pre_elo_matches_played>=20').copy()
tr=s[s.tourney_date_dt.dt.year<=2023]; va=s[s.tourney_date_dt.dt.year==2024]; te=s[s.tourney_date_dt.dt.year==2025].copy()
models={}
for name,fs in [('rank_points',['log_rank_diff','diff_player_rank_points']),('logreg19',F)]:
 p=make_pipeline(SimpleImputer(),StandardScaler(),LogisticRegression(C=.1,max_iter=2000))
 p.fit(tr[fs],tr.player_a_wins)
 if name=='logreg19':
  raw=p; cal=CalibratedClassifierCV(FrozenEstimator(p),method='sigmoid');cal.fit(va[fs],va.player_a_wins);p=cal
 models[name]=p.predict_proba(te[fs])[:,1]
models['elo_blend']=te.elo_expected_a.to_numpy();models['coin']=np.full(len(te),.5)
canonical=te.player_a_id.to_numpy()<te.player_b_id.to_numpy()
metrics=[]; bins=[]
for name,p in models.items():
 metrics.append({'model':name,'rows':int(canonical.sum()),'unique_matches':te.match_id.nunique(),'log_loss':log_loss(te.player_a_wins.to_numpy()[canonical],p[canonical]),'brier':brier_score_loss(te.player_a_wins.to_numpy()[canonical],p[canonical]),'accuracy':float(((p[canonical]>=.5)==te.player_a_wins.to_numpy()[canonical]).mean())})
 # one observation per match; transform probability into favorite probability for readable calibration
 q=p[canonical]; y=te.player_a_wins.to_numpy()[canonical]; fav=np.maximum(q,1-q); actual=((q>=.5)==y).astype(int)
 for lo,hi in [(0.5,.6),(.6,.7),(.7,.8),(.8,.9),(.9,1.00001)]:
  ix=(fav>=lo)&(fav<hi)
  bins.append({'model':name,'range':[lo,hi],'n':int(ix.sum()),'mean_pred':float(fav[ix].mean()) if ix.any() else None,'fraction_won':float(actual[ix].mean()) if ix.any() else None})
dump('evaluation.json',{'train_matches':tr.match_id.nunique(),'validation_matches':va.match_id.nunique(),'test_matches':te.match_id.nunique(),'metrics':metrics,'favorite_calibration':bins,'qualification':'New audit split on rebuilt rows; 2025 was previously inspected in notebooks, so retrospective diagnostic, not untouched confirmation.'})
te['p_cal']=models['logreg19']; te['p_elo']=models['elo_blend'];te['p_rank']=models['rank_points']
e=te[te.player_a_wins==1].merge(m[['match_id','winner_name','loser_name','score','tourney_name','round','minutes']],on='match_id',suffixes=('', '_source'))
e.sort_values('p_cal').head(15).to_csv(OUT/'largest_upsets.csv',index=False)
# Representative real match, plus point/game reversal candidates for narrative discovery.
rep=e[(e.winner_name=='Carlos Alcaraz')&(e.loser_name=='Jannik Sinner')].sort_values('tourney_date_dt')
rep.to_csv(OUT/'alcaraz_sinner_trace.csv',index=False)
reversals=m[(m.w_1stWon+m.w_2ndWon + m.l_svpt-m.l_1stWon-m.l_2ndWon)<(m.l_1stWon+m.l_2ndWon+m.w_svpt-m.w_1stWon-m.w_2ndWon)]
reversals[['match_id','winner_name','loser_name','score','tourney_name','tourney_date','round','w_svpt','w_1stWon','w_2ndWon','l_svpt','l_1stWon','l_2ndWon']].to_csv(OUT/'winner_fewer_points.csv',index=False)
dump('examples.json',{'upsets':e.sort_values('p_cal').head(8)[['match_id','tourney_date_dt','winner_name','loser_name','score','tourney_name','p_cal','p_elo','p_rank']].to_dict('records'),'alcaraz_sinner':rep[['match_id','tourney_date_dt','winner_name','loser_name','score','tourney_name','p_cal','p_elo','p_rank','a_pre_matches_last_7_days','a_pre_minutes_last_7_days']].to_dict('records'),'point_reversals':len(reversals)})
# Tournament cutoff semantics and actual prior-match inclusion.
pick=m[(m.source_year==2025)&(m.tourney_name=='Roland Garros')&(m['round']=='F')]
if len(pick):
 row=pick.iloc[0]; ss=t['player_state_snapshots']; ss=ss[ss.match_id==row.match_id]
 dump('representative_trace.json',{'source':row.to_dict(),'pre_snapshots':ss.to_dict('records'),'model_rows':rep[rep.match_id==row.match_id].to_dict('records'),'same_tournament_prior_matches':m[(m.tourney_id==row.tourney_id)&(m['round']!='F')&((m.winner_id==row.winner_id)|(m.loser_id==row.winner_id))][['winner_name','loser_name','round','minutes','tourney_date']].to_dict('records')})
# Point-series supply absent from base data: limited set-level reveal is feasible, match-point narrative is not.
dump('input_fingerprints.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('.').glob('atp_matches_20*.csv'))})
