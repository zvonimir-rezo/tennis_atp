# Engineered Features & Variables

The following predictive features are calculated dynamically by the pipeline. All features are strictly **pre-match** (using only data available before the match starts) to prevent data leakage.

## Storage Locations

Depending on the stage of the pipeline, these variables can be found in the following Parquet files in the `data/processed/` directory:

1. **`player_state_snapshots.parquet`**: Contains the state of these variables for each player exactly as it was just before each historical match they played. Columns are prefixed with `pre_` (e.g., `pre_overall_elo`).
2. **`model_training_rows.parquet`**: Contains the match-level training data for the machine learning models. It includes the `a_` and `b_` prefixed variables for both players, as well as the computed differences (`diff_`).
3. **`elo_history.parquet`**: Specifically tracks just the pre-match Elo ratings for the winner and loser of every historical match.
4. **`latest_player_state.parquet`**: Contains the most up-to-date values for every player as of the last processed match in the dataset.

---

## Calculated Variables by Category

### 1. Elo Ratings
Instead of just relying on ATP rank points, we maintain custom Elo ratings updated match-by-match.
* **`overall_elo`**: The player's overall Elo rating.
* **`surface_elo`**: The player's Elo rating specific to the surface (Hard, Clay, Grass).
* **`elo_matches_played` / `surface_elo_matches_played`**: Number of matches played under that Elo, giving a proxy for how reliable the rating is.

### 2. Form & Win Percentages (Rolling)
Calculated overall and per-surface over different time windows.
* **`win_pct_last_5`, `win_pct_last_10`, `win_pct_last_20`**: Short-term and medium-term form.
* **`win_pct_lifetime` & `surface_win_pct_lifetime`**: Career baseline metrics.
* **`surface_win_pct_last_10`**: Recent form on the specific surface.

### 3. Fatigue, Rest & Schedule
Metrics tracking how much tennis the player has played recently.
* **`days_since_last_match`**: To flag potentially tired or rusty players.
* **`matches_last_7_days`, `matches_last_14_days`, `matches_last_30_days`**: Rolling counts of matches.
* **`minutes_last_7_days`, `minutes_last_14_days`, `minutes_last_30_days`**: Rolling counts of time on court.
* **`sets_last_7_days`, `games_last_7_days`**: Volume of play.
* **`fatigue_index_v1`**: A custom composite score taking into account recent minutes played, matches played, short rest (<3 days), and deep tournament runs.
* **Momentum indicators**: `reached_sf_previous_week`, `reached_final_previous_week`, `won_title_previous_week`.
* **Retirement risks**: `retired_last_match`, `retirements_last_10_matches`, `missing_minutes_recent_flag`.

### 4. Head-to-Head (H2H)
Not just simple wins/losses, but mathematically decayed to favor recent encounters.
* **Standard H2H**: `h2h_matches`, `h2h_wins`, `h2h_win_pct`, `h2h_surface_matches`, `h2h_surface_wins`, `h2h_surface_win_pct`.
* **Time-Decayed H2H**: `h2h_decayed_wins`, `h2h_decayed_losses`, `h2h_decayed_net`. Applies an exponential decay (0.85 by default) so recent wins hold more weight than older ones.

### 5. Matchup Specifics (vs. Handedness)
How well the player does against Lefties vs Righties.
* **`matches_vs_hand`, `win_pct_vs_hand`**: Based specifically on the opponent's handedness in the upcoming match.
* **`surface_matches_vs_hand`, `surface_win_pct_vs_hand`**: Handedness matchup restricted to the current surface.

### 6. Mental Resilience (First Set Dynamics)
How players handle going ahead or falling behind.
* **`first_set_win_pct`**: How often they win the first set.
* **`win_after_winning_first_set_pct`**: Ability to close out matches after taking the lead.
* **`win_after_losing_first_set_pct`**: Ability to mount a comeback.
* **`matches_with_first_set_data`**: Sample size for these metrics.

### 7. Granular Match Stats (Rolling 20-Match Average)
Derived from the raw integer point counts (like 1st serves in, total points, aces).
* **Serve Stats**: `first_serve_in_pct`, `first_serve_points_won_pct`, `second_serve_points_won_pct`, `service_games_won_pct`, `ace_rate`, `double_fault_rate`, `service_points_won_pct`.
* **Return Stats**: `return_points_won_pct`, `return_games_won_pct`.
* **Clutch Stats**: `break_points_saved_pct`, `break_points_converted_pct`.

### 8. Match-Level Differentials (Model Input)
For the actual machine learning model (`model_training_rows.parquet`), we calculate the difference between Player A and Player B.
* **Examples**: `diff_player_rank`, `log_rank_diff`, `diff_pre_surface_elo`, `diff_pre_fatigue_index`, etc.
* **`elo_expected_a`**: A blended probability based on Overall and Surface Elos, establishing a baseline probability of winning before the ML model runs.
