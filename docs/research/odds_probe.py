"""Inspect existing rank-first odds linkage without editing production data."""
import json
from pathlib import Path
import pandas as pd
from tennis_atp_pipeline.data import load_matches
m=load_matches();o=pd.read_parquet('data/processed/odds_raw.parquet')
m['year']=m.tourney_date_dt.dt.year;o['year']=o.Match_Date.dt.year
o['WRank']=pd.to_numeric(o.WRank,errors='coerce');o['LRank']=pd.to_numeric(o.LRank,errors='coerce')
j=m.merge(o.reset_index().rename(columns={'index':'odds_idx'}),left_on=['year','winner_rank','loser_rank'],right_on=['year','WRank','LRank'])
j['date_diff']=(j.Match_Date-j.tourney_date_dt).dt.days
j=j[j.date_diff.between(-7,21)].copy();j['abs_diff']=j.date_diff.abs();j=j.sort_values('abs_diff').drop_duplicates('match_id').drop_duplicates('odds_idx')
def key(s):return str(s).lower().replace('-','').replace('.','')
# Audit only basic surname agreement. Mismatches are suspect, not all adjudicated wrong.
def compatible(a,b):
    aa=[key(v) for v in a.split()];bb=[key(v) for v in b.split()[:-1]]
    return any(x in y or y in x for x in aa for y in bb)
j['w_ok']=[compatible(a,b) for a,b in zip(j.winner_name,j.Winner)]
j['l_ok']=[compatible(a,b) for a,b in zip(j.loser_name,j.Loser)]
simple=j
bad=j[~(j.w_ok&j.l_ok)]
out={'rank_first_links':len(j),'links_checked':len(simple),'name_disagreements':len(bad),'sample':bad[['match_id','tourney_name','tourney_date','winner_name','loser_name','Winner','Loser','Tournament','Match_Date','winner_rank','loser_rank']].head(12).to_dict('records'),'provenance':{'source_files':list(o.source_file.unique()),'date_min':o.Match_Date.min(),'date_max':o.Match_Date.max()},'qualification':'Surname discrepancies flag suspect links. Compound surnames can yield false flags; no profitability claim is warranted from these links.'}
Path('reports/discovery/odds-link-audit.json').write_text(json.dumps(out,indent=2,default=str));print(json.dumps(out,indent=2,default=str))
