import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator

def train_and_save_model():
    root_dir = Path(__file__).resolve().parent.parent.parent
    data_dir = root_dir / 'data'
    models_dir = root_dir / 'models'
    models_dir.mkdir(exist_ok=True)
    
    print("Loading data...")
    df = pd.read_parquet(data_dir / 'processed/model_training_rows.parquet')
    
    # Filter to valid matches
    df = df.query('a_pre_elo_matches_played >= 20 and b_pre_elo_matches_played >= 20').copy()
    
    FEATURES = [
        'diff_pre_surface_elo', 'diff_pre_overall_elo', 'elo_expected_a',
        'diff_player_rank_points', 'diff_player_age',
        'diff_pre_win_pct_last_10', 'diff_pre_surface_win_pct_last_10',
        'diff_pre_h2h_decayed_net',
        'diff_pre_service_points_won_pct', 'diff_pre_return_points_won_pct',
        'diff_pre_win_after_winning_first_set_pct', 'diff_pre_win_after_losing_first_set_pct',
        'diff_pre_fatigue_index_v1', 'diff_pre_days_since_last_match',
        'diff_pre_matches_last_7_days', 'diff_pre_minutes_last_7_days',
        'diff_pre_retirements_last_10_matches',
        'a_is_lefty', 'b_is_lefty',
    ]
    TARGET = 'player_a_wins'
    
    X = df[FEATURES]
    y = df[TARGET].astype(int)
    
    print(f"Training on {len(X)} matches with {len(FEATURES)} features...")
    
    # We found best C = 0.1 during tuning
    pipe = Pipeline([
        ('imp', SimpleImputer(strategy='median')),
        ('sc', StandardScaler()),
        ('clf', LogisticRegression(C=0.1, max_iter=1000, solver='lbfgs'))
    ])
    
    # Train base model
    pipe.fit(X, y)
    
    # Calibrate using full dataset via CV. 
    # CalibratedClassifierCV with cv=5 will split the data, train base estimators, 
    # and fit the calibrator, returning a robust final model.
    print("Calibrating probabilities...")
    calibrated_model = CalibratedClassifierCV(estimator=pipe, method='sigmoid', cv=5)
    calibrated_model.fit(X, y)
    
    # Save the model
    model_path = models_dir / 'logreg_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(calibrated_model, f)
        
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
