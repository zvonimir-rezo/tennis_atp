import sys
from pathlib import Path
from tennis_atp_pipeline.features import build_feature_tables
from tennis_atp_pipeline.odds import append_odds

def main() -> None:
    tables = build_feature_tables(write=False)
    
    # Append odds to the training rows
    tables["model_training_rows"] = append_odds(
        tables["model_training_rows"], 
        tables["matches_normalized"]
    )
    
    # Write everything
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    import pickle
    states = dict(tables.pop("player_states_dict"))
    with open(output_dir / "player_states.pkl", "wb") as f:
        pickle.dump(states, f)
        
    for name, table in tables.items():
        print(f"{name}: {len(table):,} rows")
        table.to_parquet(output_dir / f"{name}.parquet", index=False)

if __name__ == "__main__":
    main()
