import pandas as pd
import numpy as np
from sklearn.metrics import log_loss

def main():
    df = pd.read_parquet('data/processed/model_training_rows.parquet')
    
    # Filter to matches that have odds and happened from 2022 onwards (to avoid cold-start years)
    df = df.dropna(subset=['bookmaker_odds_player_a', 'bookmaker_odds_player_b', 'elo_expected_a'])
    df = df[df['tourney_date_dt'].dt.year >= 2022]
    
    # Take one row per match
    df = df.drop_duplicates(subset=['match_id']).copy()
    
    # Filter valid decimal odds
    df = df[(df['bookmaker_odds_player_a'] > 1.0) & (df['bookmaker_odds_player_b'] > 1.0)]
    
    # Filter out matches where Elo is not fully calibrated
    df = df[(df['a_pre_elo_matches_played'] >= 20) & (df['b_pre_elo_matches_played'] >= 20)]
    
    print(f"Evaluating on {len(df)} matches (2022-2025) with odds.")
    
    # Calculate bookie implied probabilities
    bookie_implied_a = 1 / df['bookmaker_odds_player_a']
    
    # Log Loss
    elo_ll = log_loss(df['player_a_wins'], df['elo_expected_a'], labels=[0, 1])
    bookie_ll = log_loss(df['player_a_wins'], bookie_implied_a, labels=[0, 1])
    
    print(f"Pure Elo Log Loss: {elo_ll:.4f}")
    print(f"Bookie Log Loss:   {bookie_ll:.4f}")
    
    # Let's test blending Surface Elo and Overall Elo (50/50)
    # Actually, model_training_rows doesn't compute surface expected a directly,
    # but we have a_pre_surface_elo and b_pre_surface_elo.
    surface_elo_expected_a = 1 / (1 + 10 ** (-(df['a_pre_surface_elo'] - df['b_pre_surface_elo']) / 400))
    blended_expected_a = 0.5 * df['elo_expected_a'] + 0.5 * surface_elo_expected_a
    
    blended_ll = log_loss(df['player_a_wins'], blended_expected_a, labels=[0, 1])
    print(f"Blended Elo (50% Overall / 50% Surface) Log Loss: {blended_ll:.4f}")
    
    # --- SIMPLE BACKTEST ---
    print("\n--- SIMPLE VALUE BETTING BACKTEST (Blended Elo) ---")
    
    for edge_threshold in [0.0, 0.02, 0.05, 0.10]:
        edge_a = blended_expected_a - (1 / df['bookmaker_odds_player_a'])
        edge_b = (1 - blended_expected_a) - (1 / df['bookmaker_odds_player_b'])
        
        bets_a = edge_a > edge_threshold
        bets_b = edge_b > edge_threshold
        
        pl_a = np.where(df['player_a_wins'] == 1, df['bookmaker_odds_player_a'] - 1, -1) * bets_a
        pl_b = np.where(df['player_a_wins'] == 0, df['bookmaker_odds_player_b'] - 1, -1) * bets_b
        
        total_bets = bets_a.sum() + bets_b.sum()
        total_profit = pl_a.sum() + pl_b.sum()
        roi = (total_profit / total_bets) if total_bets > 0 else 0
        
        print(f"Edge Threshold: {edge_threshold*100:.0f}% -> Bets: {total_bets:<4} | Profit: {total_profit:>7.2f}u | ROI: {roi:>6.2%}")

if __name__ == "__main__":
    main()
