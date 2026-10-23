import pandas as pd
from pathlib import Path

def append_odds(model_training_rows: pd.DataFrame, matches_normalized: pd.DataFrame) -> pd.DataFrame:
    odds_path = Path('data/processed/odds_raw.parquet')
    if not odds_path.exists():
        print("odds_raw.parquet not found, skipping odds append.")
        return model_training_rows
        
    odds = pd.read_parquet(odds_path)
    odds['WRank'] = pd.to_numeric(odds['WRank'], errors='coerce')
    odds['LRank'] = pd.to_numeric(odds['LRank'], errors='coerce')

    def extract_last_name_sackmann(name):
        if pd.isna(name): return ""
        return str(name).split(' ')[-1].lower().replace('-', '')

    def extract_last_name_odds(name):
        if pd.isna(name): return ""
        return str(name).split(' ')[0].lower().replace('-', '')

    matches = matches_normalized.copy()
    matches['w_last'] = matches['winner_name'].apply(extract_last_name_sackmann)
    matches['l_last'] = matches['loser_name'].apply(extract_last_name_sackmann)

    odds['w_last'] = odds['Winner'].apply(extract_last_name_odds)
    odds['l_last'] = odds['Loser'].apply(extract_last_name_odds)

    matches['year'] = matches['tourney_date_dt'].dt.year
    odds['year'] = odds['Match_Date'].dt.year

    # Strategy 1: Rank Match
    join_rank = pd.merge(
        matches, 
        odds.reset_index().rename(columns={'index': 'odds_idx'}), 
        left_on=['year', 'winner_rank', 'loser_rank'], 
        right_on=['year', 'WRank', 'LRank'], 
        how='inner'
    )
    join_rank['date_diff'] = (join_rank['Match_Date'] - join_rank['tourney_date_dt']).dt.days
    valid_rank = join_rank[(join_rank['date_diff'] >= -7) & (join_rank['date_diff'] <= 21)].copy()
    valid_rank['abs_diff'] = valid_rank['date_diff'].abs()
    valid_rank = valid_rank.sort_values('abs_diff').drop_duplicates(subset=['match_id'])
    valid_rank = valid_rank.drop_duplicates(subset=['odds_idx'])

    matched_match_ids = set(valid_rank['match_id'])
    matched_odds_idx = set(valid_rank['odds_idx'])

    # Strategy 2: Name Match
    unjoined_matches = matches[~matches['match_id'].isin(matched_match_ids)]
    unjoined_odds = odds.reset_index().rename(columns={'index': 'odds_idx'})
    unjoined_odds = unjoined_odds[~unjoined_odds['odds_idx'].isin(matched_odds_idx)]

    join_name = pd.merge(
        unjoined_matches,
        unjoined_odds,
        left_on=['year', 'w_last', 'l_last'],
        right_on=['year', 'w_last', 'l_last'],
        how='inner'
    )
    join_name['date_diff'] = (join_name['Match_Date'] - join_name['tourney_date_dt']).dt.days
    valid_name = join_name[(join_name['date_diff'] >= -14) & (join_name['date_diff'] <= 28)].copy()
    valid_name['abs_diff'] = valid_name['date_diff'].abs()
    valid_name = valid_name.sort_values('abs_diff').drop_duplicates(subset=['match_id'])
    valid_name = valid_name.drop_duplicates(subset=['odds_idx'])

    final_odds_map = pd.concat([valid_rank, valid_name])
    
    # We want to pull B365W, B365L, PSW, PSL
    odds_map = final_odds_map[['match_id', 'B365W', 'B365L', 'PSW', 'PSL', 'AvgW', 'AvgL']].copy()
    
    # Merge onto training rows
    res = pd.merge(model_training_rows, odds_map, on='match_id', how='left')
    
    # Determine player_a and player_b odds based on who won
    # In model_training_rows, if player_a_won == 1, then player_a was the Winner.
    res['b365_a'] = pd.Series(dtype='float64')
    res['b365_b'] = pd.Series(dtype='float64')
    res['ps_a'] = pd.Series(dtype='float64')
    res['ps_b'] = pd.Series(dtype='float64')
    res['avg_a'] = pd.Series(dtype='float64')
    res['avg_b'] = pd.Series(dtype='float64')

    a_won_idx = res['player_a_wins'] == 1
    a_lost_idx = res['player_a_wins'] == 0

    res.loc[a_won_idx, 'b365_a'] = pd.to_numeric(res.loc[a_won_idx, 'B365W'], errors='coerce')
    res.loc[a_won_idx, 'b365_b'] = pd.to_numeric(res.loc[a_won_idx, 'B365L'], errors='coerce')
    res.loc[a_won_idx, 'ps_a'] = pd.to_numeric(res.loc[a_won_idx, 'PSW'], errors='coerce')
    res.loc[a_won_idx, 'ps_b'] = pd.to_numeric(res.loc[a_won_idx, 'PSL'], errors='coerce')
    res.loc[a_won_idx, 'avg_a'] = pd.to_numeric(res.loc[a_won_idx, 'AvgW'], errors='coerce')
    res.loc[a_won_idx, 'avg_b'] = pd.to_numeric(res.loc[a_won_idx, 'AvgL'], errors='coerce')

    res.loc[a_lost_idx, 'b365_a'] = pd.to_numeric(res.loc[a_lost_idx, 'B365L'], errors='coerce')
    res.loc[a_lost_idx, 'b365_b'] = pd.to_numeric(res.loc[a_lost_idx, 'B365W'], errors='coerce')
    res.loc[a_lost_idx, 'ps_a'] = pd.to_numeric(res.loc[a_lost_idx, 'PSL'], errors='coerce')
    res.loc[a_lost_idx, 'ps_b'] = pd.to_numeric(res.loc[a_lost_idx, 'PSW'], errors='coerce')
    res.loc[a_lost_idx, 'avg_a'] = pd.to_numeric(res.loc[a_lost_idx, 'AvgL'], errors='coerce')
    res.loc[a_lost_idx, 'avg_b'] = pd.to_numeric(res.loc[a_lost_idx, 'AvgW'], errors='coerce')

    # Impute missing PS odds with B365 odds, then Avg odds
    res['ps_a'] = res['ps_a'].fillna(res['b365_a']).fillna(res['avg_a'])
    res['ps_b'] = res['ps_b'].fillna(res['b365_b']).fillna(res['avg_b'])
    
    # Create final bookmaker odds column
    res['bookmaker_odds_player_a'] = res['ps_a']
    res['bookmaker_odds_player_b'] = res['ps_b']

    # Cleanup temp columns
    res = res.drop(columns=['B365W', 'B365L', 'PSW', 'PSL', 'AvgW', 'AvgL', 'b365_a', 'b365_b', 'ps_a', 'ps_b', 'avg_a', 'avg_b'])
    
    return res
