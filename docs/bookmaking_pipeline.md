# ATP Bookmaking Pipeline

## Objective

Create a pre-match ATP singles model that outputs calibrated win probabilities and fair decimal odds for both players:

```text
fair_odds_player_a = 1 / model_probability_player_a
fair_odds_player_b = 1 / model_probability_player_b
```

When bookmaker odds are available, estimate value with:

```text
implied_probability = 1 / bookmaker_decimal_odds
expected_value = model_probability * bookmaker_decimal_odds - 1
```

The first useful version should be intentionally simple: load data, create leakage-safe features, train a calibrated model, evaluate it chronologically, and expose a small prediction function for a new matchup.

## Recommended Stack

- Language: Python.
- Core data: pandas, numpy.
- Modeling: scikit-learn first.
- Baselines: logistic regression, Elo, surface Elo.
- Stronger models: histogram gradient boosting, LightGBM, CatBoost.
- Calibration: scikit-learn calibration tools, preferably time-split validation.
- Experiment tracking: start with versioned output files; add MLflow only when experiments become hard to compare manually.
- Storage: CSV input, Parquet processed tables.
- Interface: CLI first, then a small Streamlit/FastAPI app only after the model is useful.

This data volume is small enough that Spark, Airflow, Kafka, deep learning infrastructure, and a database are unnecessary at the beginning.

## Modeling State Of The Art For This Dataset

The practical state of the art for Jeff Sackmann-style pre-match tennis data is not a neural network. It is usually:

1. A strong Elo/rating backbone.
2. Surface-specific adjustment.
3. Recent-form and rolling serve/return features.
4. A probabilistic model such as logistic regression or gradient boosting.
5. Probability calibration.
6. Betting-market comparison and backtesting.

Important lessons from the literature:

- Betting odds are an extremely strong benchmark. A model that cannot beat closing odds on log loss or calibration may still be useful only if it finds a reliable subset of mispriced matches.
- Elo and surface Elo are strong, interpretable baselines. A weighted blend of overall Elo and surface-specific Elo is a natural first model.
- Serve strength and return strength matter, but they must be computed from previous matches only.
- For betting, calibration matters more than raw classification accuracy because the output is a price, not just a winner pick.

## Feature Plan

Build each row from the perspective of `player_a` versus `player_b`, with the target `player_a_wins`.

Initial features:

- Match context: surface, tournament level, best of 3/5, round, draw size.
- Player metadata: age, height, hand, country.
- Ranking: rank difference, log-rank difference, rank-points difference.
- Overall Elo before match.
- Surface Elo before match.
- Recent form: rolling win percentage over last 5, 10, 20 matches.
- Surface form: rolling surface win percentage.
- Serve quality: rolling ace rate, double-fault rate, first-serve in rate, first-serve points won, second-serve points won, service points won.
- Return quality: opponent serve points not won, break points created, return points won proxy.
- Fatigue/load: matches in previous 7/14/30 days, minutes played in previous 7/14/30 days when available.
- Head-to-head: prior H2H wins/losses and prior surface H2H, with shrinkage or low weight.
- Trend: Elo change or win-rate change over recent windows.

Avoid as first-pass features:

- Current match score, minutes, aces, serve stats, or break points.
- Post-match rankings or ranking points.
- Random train/test splits.
- Features computed using a full-season aggregate without date shifting.

## Model Progression

1. Baseline 0: higher-ranked player wins.
2. Baseline 1: logistic regression on rank/rank-points differences.
3. Baseline 2: Elo and surface Elo.
4. Model 1: logistic regression on engineered features.
5. Model 2: calibrated gradient boosting.
6. Model 3: ensemble or stacked calibration only after the above are stable.

The first production candidate should be the simplest calibrated model that passes chronological backtests.

## Evaluation

Use chronological splits:

- Train: 2021-2023.
- Validation: 2024.
- Test/backtest: 2025.
- Current inference: 2026 partial data.

Track:

- Log loss.
- Brier score.
- AUC.
- Accuracy, only as secondary context.
- Calibration by probability bucket.
- Return on investment by edge threshold.
- Closing-line comparison once odds data exists.

Backtesting rules:

- Remove bookmaker margin before comparing implied probabilities.
- Simulate fixed-stake and fractional Kelly strategies.
- Include conservative filters for low liquidity, missing data, retirements, walkovers, and extreme prices.
- Report number of bets, hit rate, ROI, drawdown, and confidence intervals.

## Deliverables To Build Next

1. `src/tennis_atp_pipeline/data.py`: load annual matches and players.
2. `src/tennis_atp_pipeline/features.py`: create leakage-safe player-match rows.
3. `src/tennis_atp_pipeline/elo.py`: maintain overall and surface Elo ratings.
4. `src/tennis_atp_pipeline/train.py`: train and calibrate baseline models.
5. `src/tennis_atp_pipeline/predict.py`: return probabilities and fair odds for a proposed matchup.
6. `tests/`: verify no current-match leakage and stable feature generation.

## Questions And Concerns

- Commercial use: the Jeff Sackmann dataset is CC BY-NC-SA. If this becomes a commercial betting product, we need a different license or separate data source.
- Odds data: to test profitability, we need historical bookmaker odds and ideally closing odds. Without odds, we can estimate fair prices but not prove edge.
- Prediction target: decide whether retired matches count as losses, are excluded, or are modeled separately.
- Scope: ATP tour-level only is good for a first pass; adding Challengers may help lower-ranked players but adds more noise.
- Ranking freshness: match files include rank at tournament date, but ranking files are better for exact weekly snapshots and current inference.
- Market reality: beating average bookmaker odds is hard; beating sharp closing lines is much harder.
- Player availability: injuries, travel, withdrawals, and motivation are not captured in the current data.

