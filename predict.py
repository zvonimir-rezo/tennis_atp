import argparse
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from datetime import datetime

# Import Elo logic
import sys
sys.path.append(str(Path(__file__).resolve().parent / "src"))
from tennis_atp_pipeline.elo import EloConfig, expected_score
from tennis_atp_pipeline.features import _state_features

def get_player_info(name, players_df, rankings_df):
    match = players_df[players_df['name'].str.lower() == name.lower()]
    if len(match) == 0:
        raise ValueError(f"Player '{name}' not found. Check spelling.")
    if len(match) > 1:
        # Pick the one with the highest current ranking or most recent dob
        match = match.iloc[0:1]
        
    p = match.iloc[0]
    pid = int(p['player_id'])
    hand = p['hand'] if pd.notna(p['hand']) else 'U'
    
    # Calculate age
    try:
        dob_str = str(int(p['dob']))
        dob = datetime.strptime(dob_str, '%Y%m%d')
        age = (datetime.now() - dob).days / 365.25
    except:
        age = 25.0 # fallback
        
    # Get rank points
    rank_match = rankings_df[rankings_df['player'] == pid]
    if len(rank_match) > 0:
        rank_points = rank_match.iloc[0]['points']
    else:
        rank_points = 0
        
    return pid, hand, age, rank_points, p['name']

def predict():
    parser = argparse.ArgumentParser(description="ATP Tennis Prediction CLI")
    parser.add_argument("--p1", type=str, required=True, help="Player 1 name (e.g., 'Novak Djokovic')")
    parser.add_argument("--p2", type=str, required=True, help="Player 2 name (e.g., 'Carlos Alcaraz')")
    parser.add_argument("--surface", type=str, default="Hard", choices=["Hard", "Clay", "Grass"], help="Surface")
    parser.add_argument("--odds1", type=float, help="Bookmaker odds for Player 1 (decimal)")
    parser.add_argument("--odds2", type=float, help="Bookmaker odds for Player 2 (decimal)")
    args = parser.parse_args()

def run_prediction(name1, name2, surface, odds1=None, odds2=None):
    root_dir = Path(__file__).resolve().parent
    
    # Load data
    players_df = pd.read_csv(root_dir / 'atp_players.csv')
    players_df['name'] = players_df['name_first'] + ' ' + players_df['name_last']
    rankings_df = pd.read_csv(root_dir / 'atp_rankings_current.csv')
    
    with open(root_dir / 'data/processed/player_states.pkl', 'rb') as f:
        states = pickle.load(f)
        
    with open(root_dir / 'models/logreg_model.pkl', 'rb') as f:
        model = pickle.load(f)

    id1, hand1, age1, pts1, name1 = get_player_info(name1, players_df, rankings_df)
    id2, hand2, age2, pts2, name2 = get_player_info(name2, players_df, rankings_df)
    
    state1 = states.get(id1)
    state2 = states.get(id2)
    
    warnings = []
    if not state1 or len(state1.matches) < 20:
        warnings.append(f"{name1} has fewer than 20 ATP matches on record. Model confidence is LOW.")
    if not state2 or len(state2.matches) < 20:
        warnings.append(f"{name2} has fewer than 20 ATP matches on record. Model confidence is LOW.")
        
    date = pd.Timestamp.now()
    elo_config = EloConfig()
    
    f1 = _state_features(state1, id2, hand2, surface, date, elo_config) if state1 else None
    f2 = _state_features(state2, id1, hand1, surface, date, elo_config) if state2 else None
    
    def get_f(f_dict, key, default=0.0):
        if not f_dict: return default
        val = f_dict.get(key)
        return val if pd.notna(val) else default

    features = {
        'diff_pre_surface_elo': get_f(f1, 'surface_elo', 1500) - get_f(f2, 'surface_elo', 1500),
        'diff_pre_overall_elo': get_f(f1, 'overall_elo', 1500) - get_f(f2, 'overall_elo', 1500),
        'elo_expected_a': expected_score(get_f(f1, 'overall_elo', 1500), get_f(f2, 'overall_elo', 1500)),
        'diff_player_rank_points': pts1 - pts2,
        'diff_player_age': age1 - age2,
        'diff_pre_win_pct_last_10': get_f(f1, 'win_pct_last_10', 0.5) - get_f(f2, 'win_pct_last_10', 0.5),
        'diff_pre_surface_win_pct_last_10': get_f(f1, 'surface_win_pct_last_10', 0.5) - get_f(f2, 'surface_win_pct_last_10', 0.5),
        'diff_pre_h2h_decayed_net': get_f(f1, 'h2h_decayed_net', 0.0) - get_f(f2, 'h2h_decayed_net', 0.0),
        'diff_pre_service_points_won_pct': get_f(f1, 'service_points_won_pct', 0.6) - get_f(f2, 'service_points_won_pct', 0.6),
        'diff_pre_return_points_won_pct': get_f(f1, 'return_points_won_pct', 0.38) - get_f(f2, 'return_points_won_pct', 0.38),
        'diff_pre_win_after_winning_first_set_pct': get_f(f1, 'win_after_winning_first_set_pct', 0.8) - get_f(f2, 'win_after_winning_first_set_pct', 0.8),
        'diff_pre_win_after_losing_first_set_pct': get_f(f1, 'win_after_losing_first_set_pct', 0.2) - get_f(f2, 'win_after_losing_first_set_pct', 0.2),
        'diff_pre_fatigue_index_v1': get_f(f1, 'fatigue_index_v1', 0.0) - get_f(f2, 'fatigue_index_v1', 0.0),
        'diff_pre_days_since_last_match': get_f(f1, 'days_since_last_match', 7) - get_f(f2, 'days_since_last_match', 7),
        'diff_pre_matches_last_7_days': get_f(f1, 'matches_last_7_days', 0) - get_f(f2, 'matches_last_7_days', 0),
        'diff_pre_minutes_last_7_days': get_f(f1, 'minutes_last_7_days', 0) - get_f(f2, 'minutes_last_7_days', 0),
        'diff_pre_retirements_last_10_matches': get_f(f1, 'retirements_last_10_matches', 0) - get_f(f2, 'retirements_last_10_matches', 0),
        'a_is_lefty': 1 if hand1 == 'L' else 0,
        'b_is_lefty': 1 if hand2 == 'L' else 0,
    }
    
    if get_f(f1, 'fatigue_index_v1') > 500:
        warnings.append(f"{name1} has a high fatigue index ({int(get_f(f1, 'fatigue_index_v1'))}).")
    if get_f(f2, 'fatigue_index_v1') > 500:
        warnings.append(f"{name2} has a high fatigue index ({int(get_f(f2, 'fatigue_index_v1'))}).")

    ordered_cols = [
        'diff_pre_surface_elo', 'diff_pre_overall_elo', 'elo_expected_a',
        'diff_player_rank_points', 'diff_player_age',
        'diff_pre_win_pct_last_10', 'diff_pre_surface_win_pct_last_10',
        'diff_pre_h2h_decayed_net',
        'diff_pre_service_points_won_pct', 'diff_pre_return_points_won_pct',
        'diff_pre_win_after_winning_first_set_pct', 'diff_pre_win_after_losing_first_set_pct',
        'diff_pre_fatigue_index_v1', 'diff_pre_days_since_last_match',
        'diff_pre_matches_last_7_days', 'diff_pre_minutes_last_7_days',
        'diff_pre_retirements_last_10_matches',
        'a_is_lefty', 'b_is_lefty'
    ]
    
    X = pd.DataFrame([{col: features[col] for col in ordered_cols}])
    
    prob1 = float(model.predict_proba(X)[0][1])
    prob2 = 1.0 - prob1
    
    fair_odds1 = 1 / prob1 if prob1 > 0 else np.inf
    fair_odds2 = 1 / prob2 if prob2 > 0 else np.inf
    
    result = {
        "player1": name1,
        "player2": name2,
        "surface": surface,
        "prob1": prob1,
        "prob2": prob2,
        "fair_odds1": fair_odds1,
        "fair_odds2": fair_odds2,
        "warnings": warnings,
        "betting_analysis": None
    }

    if odds1 and odds2:
        ev1 = (prob1 * odds1) - 1.0
        ev2 = (prob2 * odds2) - 1.0
        
        analysis = {"edge_player": None, "ev": 0, "kelly_fraction": 0}
        if ev1 > 0:
            kelly1 = (prob1 * odds1 - 1) / (odds1 - 1)
            analysis = {"edge_player": name1, "ev": ev1, "kelly_fraction": kelly1}
        elif ev2 > 0:
            kelly2 = (prob2 * odds2 - 1) / (odds2 - 1)
            analysis = {"edge_player": name2, "ev": ev2, "kelly_fraction": kelly2}
        result["betting_analysis"] = analysis

    return result

def predict():
    parser = argparse.ArgumentParser(description="ATP Tennis Prediction CLI")
    parser.add_argument("--p1", type=str, required=True, help="Player 1 name (e.g., 'Novak Djokovic')")
    parser.add_argument("--p2", type=str, required=True, help="Player 2 name (e.g., 'Carlos Alcaraz')")
    parser.add_argument("--surface", type=str, default="Hard", choices=["Hard", "Clay", "Grass"], help="Surface")
    parser.add_argument("--odds1", type=float, help="Bookmaker odds for Player 1 (decimal)")
    parser.add_argument("--odds2", type=float, help="Bookmaker odds for Player 2 (decimal)")
    args = parser.parse_args()

    result = run_prediction(args.p1, args.p2, args.surface, args.odds1, args.odds2)
    
    print("\n" + "="*50)
    print(f"MATCH: {result['player1']} vs {result['player2']} | Surface: {result['surface']}")
    print("="*50)
    for warning in result["warnings"]:
        print(f"[WARNING] {warning}")
    print(f"{result['player1']:.<30} {result['prob1']:.1%} (Fair Odds: {result['fair_odds1']:.2f})")
    print(f"{result['player2']:.<30} {result['prob2']:.1%} (Fair Odds: {result['fair_odds2']:.2f})")
    print("="*50)
    
    if result["betting_analysis"]:
        ba = result["betting_analysis"]
        print("\nBETTING ANALYSIS:")
        if ba["edge_player"]:
            print(f"✅ EDGE FOUND: {ba['edge_player']}")
            print(f"   Expected Value: +{ba['ev']:.1%}")
            print(f"   Rec. Bet Size (Kelly): {ba['kelly_fraction']/4:.2%} of bankroll (quarter Kelly)")
        else:
            print("❌ NO EDGE FOUND for either player at these odds.")
    print()

if __name__ == "__main__":
    predict()
