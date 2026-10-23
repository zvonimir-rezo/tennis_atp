import pandas as pd
from pathlib import Path

def export_current_elos():
    root_dir = Path(__file__).resolve().parent.parent.parent
    data_dir = root_dir / 'data'
    
    # Load player mappings
    players = pd.read_csv(root_dir / 'atp_players.csv')
    players['name'] = players['name_first'] + ' ' + players['name_last']
    
    # Load latest state
    state = pd.read_parquet(data_dir / 'processed/latest_player_state.parquet')
    
    # Merge and format
    merged = pd.merge(state, players[['player_id', 'name']], on='player_id', how='inner')
    
    # Sort by overall Elo descending
    merged = merged.sort_values('overall_elo', ascending=False)
    
    # Filter to players with at least 10 matches so the list isn't cluttered with unrated players
    merged = merged[merged['matches_played'] >= 10]
    
    # Format the dataframe
    output_df = merged[['name', 'overall_elo', 'hard_elo', 'clay_elo', 'grass_elo', 'matches_played', 'last_match_date']]
    output_df.columns = ['Player', 'Overall Elo', 'Hard Elo', 'Clay Elo', 'Grass Elo', 'Matches Played', 'Last Match Date']
    
    # Round Elos
    for col in ['Overall Elo', 'Hard Elo', 'Clay Elo', 'Grass Elo']:
        output_df[col] = output_df[col].round(1)
        
    output_df['Last Match Date'] = pd.to_datetime(output_df['Last Match Date']).dt.date
    
    out_path = root_dir / 'current_elos.csv'
    output_df.to_csv(out_path, index=False)
    print(f"Exported {len(output_df)} ranked players to {out_path}")

if __name__ == "__main__":
    export_current_elos()
