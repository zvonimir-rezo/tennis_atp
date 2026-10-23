# Project Guidelines

## Goal

Build a simple, reproducible ATP singles betting pipeline that:

- Loads Jeff Sackmann ATP data.
- Creates pre-match features only from information available before match start.
- Trains calibrated win-probability models.
- Converts probabilities into fair decimal odds.
- Compares fair odds with bookmaker odds when those are added.

## Modeling Rules

- Treat data leakage as the main failure mode.
- Do not use match outcome, score, minutes, or current-match stats as direct features for that same match.
- Rolling features must be shifted so the current match is excluded.
- Prefer chronological train/validation/test splits over random splits.
- Evaluate probabilities with log loss, Brier score, calibration curves, and expected value backtests.
- Accuracy is secondary; betting decisions need calibrated probabilities.
- Keep a strong baseline: rank/rank-points model, Elo model, then ML model.

## Data Scope

- Default match scope: `atp_matches_2017.csv` through `atp_matches_2025.csv`.
- Include `atp_matches_2026.csv` for current-season inference or explicitly partial-season validation.
- Use `atp_players.csv` for stable player metadata.
- Use `atp_rankings_current.csv` for current ranking snapshots when needed.
- Ignore doubles, futures, and challengers unless the task explicitly expands the scope.

## Implementation Style

- Keep the pipeline small and scriptable before adding orchestration.
- Prefer plain Python modules, pandas, numpy, and scikit-learn first.
- Add LightGBM/CatBoost only after the baseline is reproducible.
- Store generated outputs under ignored directories such as `data/processed/`, `models/`, and `reports/`.
- Do not modify the upstream CSV files.
