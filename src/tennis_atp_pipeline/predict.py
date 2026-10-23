from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from tennis_atp_pipeline.elo import EloConfig, expected_score
from tennis_atp_pipeline.features import PlayerState, _state_features
from tennis_atp_pipeline.paths import MODELS_DIR, PROCESSED_DIR


def _latest_player_row(training_rows: pd.DataFrame, player_id: int) -> pd.Series:
    rows = training_rows[training_rows["player_a_id"] == player_id].sort_values("tourney_date_dt")
    if rows.empty:
        raise ValueError(f"No historical state found for player_id={player_id}")
    return rows.iloc[-1]


def _player_hand(history: pd.DataFrame) -> str:
    hands = history["hand"].dropna()
    return str(hands.iloc[-1]) if not hands.empty else ""


def _build_player_state(
    player_id: int,
    history: pd.DataFrame,
    latest_state: pd.DataFrame,
) -> PlayerState:
    state_row = latest_state[latest_state["player_id"] == player_id]
    if state_row.empty:
        raise ValueError(f"No latest state found for player_id={player_id}")
    state_row = state_row.iloc[0]
    state = PlayerState(overall_elo=float(state_row["overall_elo"]))
    for surface in ("Hard", "Clay", "Grass", "Carpet"):
        column = f"{surface.lower()}_elo"
        if column in state_row and not pd.isna(state_row[column]):
            state.surface_elo[surface] = float(state_row[column])

    records = []
    player_history = history[history["player_id"] == player_id].sort_values("date")
    for _, row in player_history.iterrows():
        record = row.to_dict()
        record["date"] = pd.to_datetime(record["date"])
        record["won"] = bool(record["won"])
        record["retired"] = bool(record.get("retired", False))
        records.append(record)
        state.h2h[int(record["opponent_id"])].append(record)
    state.matches = records
    return state


def _snapshot_for_upcoming(
    player_id: int,
    opponent_id: int,
    opponent_hand: str,
    surface: str,
    match_date: pd.Timestamp,
    history: pd.DataFrame,
    latest_state: pd.DataFrame,
    training_rows: pd.DataFrame,
) -> dict[str, Any]:
    state = _build_player_state(player_id, history, latest_state)
    features = _state_features(state, opponent_id, opponent_hand, surface, match_date, EloConfig())
    latest = _latest_player_row(training_rows, player_id)
    row = {
        "player_id": player_id,
        "player_rank": latest.get("a_player_rank", np.nan),
        "player_rank_points": latest.get("a_player_rank_points", np.nan),
        "player_age": latest.get("a_player_age", np.nan),
        "player_hand": latest.get("a_player_hand", np.nan),
    }
    row.update({f"pre_{key}": value for key, value in features.items()})
    return row


def build_upcoming_match_row(
    player_a_id: int,
    player_b_id: int,
    surface: str,
    tourney_level: str = "A",
    round_name: str = "R32",
    best_of: int = 3,
    draw_size: int | float = np.nan,
    match_date: str | pd.Timestamp | None = None,
    processed_dir: Path = PROCESSED_DIR,
) -> pd.DataFrame:
    training_rows = pd.read_parquet(processed_dir / "model_training_rows.parquet")
    training_rows["tourney_date_dt"] = pd.to_datetime(training_rows["tourney_date_dt"])
    history = pd.read_parquet(processed_dir / "player_match_history.parquet")
    history["date"] = pd.to_datetime(history["date"])
    latest_state = pd.read_parquet(processed_dir / "latest_player_state.parquet")
    match_date = (
        pd.to_datetime(match_date)
        if match_date is not None
        else pd.to_datetime(training_rows["tourney_date_dt"].max())
    )

    a_history = history[history["player_id"] == player_a_id]
    b_history = history[history["player_id"] == player_b_id]
    a_hand = _player_hand(a_history)
    b_hand = _player_hand(b_history)
    a = _snapshot_for_upcoming(
        player_a_id,
        player_b_id,
        b_hand,
        surface,
        match_date,
        history,
        latest_state,
        training_rows,
    )
    b = _snapshot_for_upcoming(
        player_b_id,
        player_a_id,
        a_hand,
        surface,
        match_date,
        history,
        latest_state,
        training_rows,
    )

    row: dict[str, Any] = {
        "surface": surface,
        "tourney_level": tourney_level,
        "round": round_name,
        "best_of": best_of,
        "draw_size": draw_size,
        "player_a_id": player_a_id,
        "player_b_id": player_b_id,
    }
    for column in training_rows.columns:
        if column.startswith("a_"):
            base_column = column[2:]
            row[column] = a.get(base_column, np.nan)
            b_column = f"b_{base_column}"
            row[b_column] = b.get(base_column, np.nan)
            diff_column = f"diff_{base_column}"
            if diff_column in training_rows.columns:
                row[diff_column] = row[column] - row[b_column]

    row["rank_diff"] = row.get("a_player_rank", np.nan) - row.get("b_player_rank", np.nan)
    row["log_rank_diff"] = (
        np.log(row["a_player_rank"] + 1) - np.log(row["b_player_rank"] + 1)
        if not pd.isna(row.get("a_player_rank")) and not pd.isna(row.get("b_player_rank"))
        else np.nan
    )
    row["same_hand_matchup"] = int(row.get("a_is_lefty") == row.get("b_is_lefty"))
    elo_a = 0.5 * row.get("a_pre_overall_elo", 1500.0) + 0.5 * row.get(
        "a_pre_surface_elo", 1500.0
    )
    elo_b = 0.5 * row.get("b_pre_overall_elo", 1500.0) + 0.5 * row.get(
        "b_pre_surface_elo", 1500.0
    )
    row["elo_expected_a"] = expected_score(elo_a, elo_b)
    return pd.DataFrame([row])


def price_match(
    player_a_id: int,
    player_b_id: int,
    surface: str,
    tourney_level: str = "A",
    round_name: str = "R32",
    best_of: int = 3,
    draw_size: int | float = np.nan,
    match_date: str | pd.Timestamp | None = None,
    model_path: Path = MODELS_DIR / "calibrated_model.joblib",
    metadata_path: Path = MODELS_DIR / "feature_metadata.json",
) -> dict[str, float | int | str]:
    model = joblib.load(model_path)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    row = build_upcoming_match_row(
        player_a_id=player_a_id,
        player_b_id=player_b_id,
        surface=surface,
        tourney_level=tourney_level,
        round_name=round_name,
        best_of=best_of,
        draw_size=draw_size,
        match_date=match_date,
    )
    feature_columns = metadata["numeric_features"] + metadata["categorical_features"]
    probability_a = float(model.predict_proba(row[feature_columns])[:, 1][0])
    probability_b = 1.0 - probability_a
    return {
        "player_a_id": player_a_id,
        "player_b_id": player_b_id,
        "model_probability_player_a": probability_a,
        "model_probability_player_b": probability_b,
        "fair_decimal_odds_player_a": 1.0 / probability_a,
        "fair_decimal_odds_player_b": 1.0 / probability_b,
    }
