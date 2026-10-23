from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from math import log
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from tennis_atp_pipeline.data import load_matches
from tennis_atp_pipeline.elo import EloConfig, expected_score, update_elo, calculate_k_factor
from tennis_atp_pipeline.paths import PROCESSED_DIR, SURFACES, ensure_output_dirs


def _default_surface_elo_value():
    return 1500.0

def _default_surface_elo():
    return defaultdict(_default_surface_elo_value)

def _default_h2h():
    return defaultdict(list)

@dataclass
class PlayerState:
    overall_elo: float = 1500.0
    surface_elo: dict[str, float] = field(default_factory=_default_surface_elo)
    matches: list[dict[str, Any]] = field(default_factory=list)
    h2h: dict[int, list[dict[str, Any]]] = field(default_factory=_default_h2h)


def _safe_div(num: float | int | None, den: float | int | None) -> float:
    if den is None or pd.isna(den) or den == 0 or num is None or pd.isna(num):
        return np.nan
    return float(num) / float(den)


def _rate(records: list[dict[str, Any]], key: str, window: int | None = None) -> float:
    values = [r[key] for r in (records[-window:] if window else records) if r.get(key) is not None]
    if not values:
        return np.nan
    return float(np.mean(values))


def _sum_since(
    records: list[dict[str, Any]], current_date: pd.Timestamp, days: int, key: str
) -> float:
    cutoff = current_date - pd.Timedelta(days=days)
    values = [
        r.get(key, 0.0)
        for r in records
        if r.get("date") is not None
        and cutoff <= r["date"] < current_date
        and not pd.isna(r.get(key, np.nan))
    ]
    return float(np.sum(values)) if values else 0.0


def _count_since(records: list[dict[str, Any]], current_date: pd.Timestamp, days: int) -> int:
    cutoff = current_date - pd.Timedelta(days=days)
    return sum(
        1 for r in records if r.get("date") is not None and cutoff <= r["date"] < current_date
    )


def _last_date(records: list[dict[str, Any]]) -> pd.Timestamp | None:
    return records[-1]["date"] if records else None


def _round_flag(records: list[dict[str, Any]], current_date: pd.Timestamp, round_name: str) -> int:
    cutoff = current_date - pd.Timedelta(days=7)
    return int(
        any(
            r.get("date") is not None
            and cutoff <= r["date"] < current_date
            and str(r.get("round", "")).upper() == round_name
            for r in records
        )
    )


def _decayed_h2h(
    records: list[dict[str, Any]], surface: str | None = None, decay: float = 0.85
) -> dict[str, float]:
    filtered = [r for r in records if surface is None or r.get("surface") == surface]
    wins = 0.0
    losses = 0.0
    for idx, record in enumerate(reversed(filtered)):
        weight = decay**idx
        if record["won"]:
            wins += weight
        else:
            losses += weight
    matches = len(filtered)
    return {
        "matches": matches,
        "wins": sum(1 for r in filtered if r["won"]),
        "win_pct": _safe_div(sum(1 for r in filtered if r["won"]), matches),
        "decayed_wins": wins,
        "decayed_losses": losses,
        "decayed_net": wins - losses,
    }


def _state_features(
    state: PlayerState,
    opponent_id: int,
    opponent_hand: str,
    surface: str,
    date: pd.Timestamp,
    elo_config: EloConfig,
) -> dict[str, Any]:
    records = state.matches
    last = _last_date(records)
    days_since = (date - last).days if last is not None and not pd.isna(date) else np.nan
    same_date = int(last == date) if last is not None else 0
    recent_minutes_missing = any(
        r.get("date") is not None
        and date - pd.Timedelta(days=7) <= r["date"] < date
        and r.get("minutes_missing", 0) == 1
        for r in records
    )
    h2h = _decayed_h2h(state.h2h[opponent_id])
    h2h_surface = _decayed_h2h(state.h2h[opponent_id], surface)
    vs_hand = [r for r in records if r.get("opponent_hand") == opponent_hand]
    vs_hand_surface = [r for r in vs_hand if r.get("surface") == surface]
    surface_records = [r for r in records if r.get("surface") == surface]
    first_set_records = [r for r in records if r.get("first_set_won") is not None]
    first_set_won_records = [r for r in first_set_records if r["first_set_won"]]
    first_set_lost_records = [r for r in first_set_records if not r["first_set_won"]]

    minutes_last_7 = _sum_since(records, date, 7, "minutes")
    matches_last_7 = _count_since(records, date, 7)
    short_rest_flag = int(not pd.isna(days_since) and days_since <= 3)
    reached_sf = _round_flag(records, date, "SF")
    reached_final = _round_flag(records, date, "F")
    retired_last_match = int(records[-1].get("retired", False)) if records else 0
    fatigue_index = (
        0.35 * min(minutes_last_7 / 600.0, 2.0)
        + 0.25 * min(matches_last_7 / 5.0, 2.0)
        + 0.15 * short_rest_flag
        + 0.10 * reached_sf
        + 0.10 * reached_final
        + 0.05 * retired_last_match
    )

    return {
        "overall_elo": state.overall_elo,
        "surface_elo": state.surface_elo[surface],
        "elo_matches_played": len(records),
        "surface_elo_matches_played": len(surface_records),
        "win_pct_lifetime": _rate(records, "won"),
        "win_pct_last_5": _rate(records, "won", 5),
        "win_pct_last_10": _rate(records, "won", 10),
        "win_pct_last_20": _rate(records, "won", 20),
        "surface_win_pct_lifetime": _rate(surface_records, "won"),
        "surface_win_pct_last_10": _rate(surface_records, "won", 10),
        "days_since_last_match": days_since,
        "played_on_same_tourney_date": same_date,
        "matches_last_7_days": matches_last_7,
        "matches_last_14_days": _count_since(records, date, 14),
        "matches_last_30_days": _count_since(records, date, 30),
        "minutes_last_7_days": minutes_last_7,
        "minutes_last_14_days": _sum_since(records, date, 14, "minutes"),
        "minutes_last_30_days": _sum_since(records, date, 30, "minutes"),
        "minutes_last_3_matches": float(
            np.nansum([r.get("minutes", np.nan) for r in records[-3:]])
        ),
        "sets_last_7_days": _sum_since(records, date, 7, "sets_played"),
        "games_last_7_days": _sum_since(records, date, 7, "games_played"),
        "reached_sf_previous_week": reached_sf,
        "reached_final_previous_week": reached_final,
        "won_title_previous_week": int(
            any(
                r.get("date") is not None
                and date - pd.Timedelta(days=7) <= r["date"] < date
                and str(r.get("round", "")).upper() == "F"
                and r.get("won")
                for r in records
            )
        ),
        "retired_last_match": retired_last_match,
        "retirements_last_10_matches": sum(1 for r in records[-10:] if r.get("retired", False)),
        "missing_minutes_recent_flag": int(recent_minutes_missing),
        "fatigue_index_v1": fatigue_index,
        "h2h_matches": h2h["matches"],
        "h2h_wins": h2h["wins"],
        "h2h_win_pct": h2h["win_pct"],
        "h2h_surface_matches": h2h_surface["matches"],
        "h2h_surface_wins": h2h_surface["wins"],
        "h2h_surface_win_pct": h2h_surface["win_pct"],
        "h2h_decayed_wins": h2h["decayed_wins"],
        "h2h_decayed_losses": h2h["decayed_losses"],
        "h2h_decayed_net": h2h["decayed_net"],
        "matches_vs_hand": len(vs_hand),
        "win_pct_vs_hand": _rate(vs_hand, "won"),
        "surface_matches_vs_hand": len(vs_hand_surface),
        "surface_win_pct_vs_hand": _rate(vs_hand_surface, "won"),
        "first_set_win_pct": _rate(first_set_records, "first_set_won"),
        "win_after_winning_first_set_pct": _rate(first_set_won_records, "won"),
        "win_after_losing_first_set_pct": _rate(first_set_lost_records, "won"),
        "matches_with_first_set_data": len(first_set_records),
        "service_points_won_pct": _rate(records, "service_points_won_pct", 20),
        "first_serve_in_pct": _rate(records, "first_serve_in_pct", 20),
        "first_serve_points_won_pct": _rate(records, "first_serve_points_won_pct", 20),
        "second_serve_points_won_pct": _rate(records, "second_serve_points_won_pct", 20),
        "ace_rate": _rate(records, "ace_rate", 20),
        "double_fault_rate": _rate(records, "double_fault_rate", 20),
        "service_games_won_pct": _rate(records, "service_games_won_pct", 20),
        "return_points_won_pct": _rate(records, "return_points_won_pct", 20),
        "return_games_won_pct": _rate(records, "return_games_won_pct", 20),
        "break_points_saved_pct": _rate(records, "break_points_saved_pct", 20),
        "break_points_converted_pct": _rate(records, "break_points_converted_pct", 20),
    }


def _player_stats(row: pd.Series, prefix: str) -> dict[str, Any]:
    opp = "l" if prefix == "w" else "w"
    svpt = row.get(f"{prefix}_svpt")
    first_in = row.get(f"{prefix}_1stIn")
    first_won = row.get(f"{prefix}_1stWon")
    second_won = row.get(f"{prefix}_2ndWon")
    aces = row.get(f"{prefix}_ace")
    dfs = row.get(f"{prefix}_df")
    sv_gms = row.get(f"{prefix}_SvGms")
    bp_saved = row.get(f"{prefix}_bpSaved")
    bp_faced = row.get(f"{prefix}_bpFaced")
    opp_svpt = row.get(f"{opp}_svpt")
    opp_first_won = row.get(f"{opp}_1stWon")
    opp_second_won = row.get(f"{opp}_2ndWon")
    opp_sv_gms = row.get(f"{opp}_SvGms")
    opp_bp_saved = row.get(f"{opp}_bpSaved")
    opp_bp_faced = row.get(f"{opp}_bpFaced")
    service_points_won = (first_won if not pd.isna(first_won) else 0) + (
        second_won if not pd.isna(second_won) else 0
    )
    opp_service_points_won = (opp_first_won if not pd.isna(opp_first_won) else 0) + (
        opp_second_won if not pd.isna(opp_second_won) else 0
    )
    times_broken = (
        bp_faced - bp_saved if not pd.isna(bp_faced) and not pd.isna(bp_saved) else np.nan
    )
    opp_times_broken = (
        opp_bp_faced - opp_bp_saved
        if not pd.isna(opp_bp_faced) and not pd.isna(opp_bp_saved)
        else np.nan
    )
    return {
        "service_points_won_pct": _safe_div(service_points_won, svpt),
        "first_serve_in_pct": _safe_div(first_in, svpt),
        "first_serve_points_won_pct": _safe_div(first_won, first_in),
        "second_serve_points_won_pct": _safe_div(
            second_won, svpt - first_in if not pd.isna(svpt) and not pd.isna(first_in) else np.nan
        ),
        "ace_rate": _safe_div(aces, svpt),
        "double_fault_rate": _safe_div(dfs, svpt),
        "service_games_won_pct": _safe_div(
            sv_gms - times_broken if not pd.isna(times_broken) and not pd.isna(sv_gms) else np.nan,
            sv_gms,
        ),
        "break_points_saved_pct": _safe_div(bp_saved, bp_faced),
        "return_points_won_pct": _safe_div(
            opp_svpt - opp_service_points_won if not pd.isna(opp_svpt) else np.nan, opp_svpt
        ),
        "return_games_won_pct": _safe_div(opp_times_broken, opp_sv_gms),
        "break_points_converted_pct": _safe_div(opp_times_broken, opp_bp_faced),
    }


def _history_record(row: pd.Series, is_winner: bool) -> dict[str, Any]:
    prefix = "w" if is_winner else "l"
    first_set_winner_won = row.get("score_first_set_winner_won")
    first_set_won = None
    if first_set_winner_won is not None and not pd.isna(first_set_winner_won):
        first_set_won = bool(first_set_winner_won) if is_winner else not bool(first_set_winner_won)
    games_won = row["score_winner_games_won"] if is_winner else row["score_loser_games_won"]
    games_lost = row["score_loser_games_won"] if is_winner else row["score_winner_games_won"]
    record = {
        "match_id": row["match_id"],
        "player_id": int(row[f"{'winner' if is_winner else 'loser'}_id"]),
        "opponent_id": int(row[f"{'loser' if is_winner else 'winner'}_id"]),
        "date": row["tourney_date_dt"],
        "tourney_date": row["tourney_date"],
        "surface": row["surface"],
        "tourney_level": row["tourney_level"],
        "round": row["round"],
        "best_of": row["best_of"],
        "won": bool(is_winner),
        "rank": row[f"{'winner' if is_winner else 'loser'}_rank"],
        "opponent_rank": row[f"{'loser' if is_winner else 'winner'}_rank"],
        "rank_points": row[f"{'winner' if is_winner else 'loser'}_rank_points"],
        "opponent_rank_points": row[f"{'loser' if is_winner else 'winner'}_rank_points"],
        "hand": row[f"{'winner' if is_winner else 'loser'}_hand"],
        "opponent_hand": row[f"{'loser' if is_winner else 'winner'}_hand"],
        "minutes": 0.0 if pd.isna(row.get("minutes")) else float(row.get("minutes")),
        "minutes_missing": int(pd.isna(row.get("minutes"))),
        "sets_played": row.get("score_sets_played", np.nan),
        "games_played": games_won + games_lost
        if not pd.isna(games_won) and not pd.isna(games_lost)
        else np.nan,
        "first_set_won": first_set_won,
        "retired": bool(row.get("is_retirement", False)),
    }
    record.update(_player_stats(row, prefix))
    return record


def _snapshot_row(
    match: pd.Series, player_role: str, state_features: dict[str, Any]
) -> dict[str, Any]:
    prefix = "winner" if player_role == "winner" else "loser"
    opp_prefix = "loser" if player_role == "winner" else "winner"
    row = {
        "match_id": match["match_id"],
        "tourney_date": match["tourney_date"],
        "tourney_date_dt": match["tourney_date_dt"],
        "surface": match["surface"],
        "player_id": int(match[f"{prefix}_id"]),
        "opponent_id": int(match[f"{opp_prefix}_id"]),
        "player_won": int(player_role == "winner"),
        "player_rank": match[f"{prefix}_rank"],
        "opponent_rank": match[f"{opp_prefix}_rank"],
        "player_rank_points": match[f"{prefix}_rank_points"],
        "opponent_rank_points": match[f"{opp_prefix}_rank_points"],
        "player_hand": match[f"{prefix}_hand"],
        "opponent_hand": match[f"{opp_prefix}_hand"],
        "player_age": match[f"{prefix}_age"],
        "opponent_age": match[f"{opp_prefix}_age"],
    }
    row.update({f"pre_{k}": v for k, v in state_features.items()})
    return row


def _training_row(
    match: pd.Series, a: dict[str, Any], b: dict[str, Any], a_is_winner: bool, elo_config: EloConfig
) -> dict[str, Any]:
    row = {
        "match_id": match["match_id"],
        "tourney_date": match["tourney_date"],
        "tourney_date_dt": match["tourney_date_dt"],
        "tourney_name": match["tourney_name"],
        "surface": match["surface"],
        "tourney_level": match["tourney_level"],
        "draw_size": match["draw_size"],
        "round": match["round"],
        "best_of": match["best_of"],
        "is_retirement": int(match["is_retirement"]),
        "player_a_id": a["player_id"],
        "player_b_id": b["player_id"],
        "player_a_wins": int(a_is_winner),
    }
    for col in [
        "player_rank",
        "player_rank_points",
        "player_age",
        "pre_overall_elo",
        "pre_surface_elo",
        "pre_elo_matches_played",
        "pre_win_pct_last_10",
        "pre_surface_win_pct_last_10",
        "pre_fatigue_index_v1",
        "pre_h2h_matches",
        "pre_h2h_surface_matches",
        "pre_h2h_decayed_net",
        "pre_matches_vs_hand",
        "pre_surface_matches_vs_hand",
        "pre_win_pct_vs_hand",
        "pre_matches_with_first_set_data",
        "pre_service_points_won_pct",
        "pre_return_points_won_pct",
        "pre_service_games_won_pct",
        "pre_return_games_won_pct",
        "pre_win_after_winning_first_set_pct",
        "pre_win_after_losing_first_set_pct",
        "pre_days_since_last_match",
        "pre_matches_last_7_days",
        "pre_minutes_last_7_days",
        "pre_retirements_last_10_matches",
    ]:
        a_val = a.get(col, np.nan)
        b_val = b.get(col, np.nan)
        row[f"a_{col}"] = a_val
        row[f"b_{col}"] = b_val
        if pd.api.types.is_number(a_val) or pd.api.types.is_number(b_val):
            row[f"diff_{col}"] = a_val - b_val
    row["a_is_lefty"] = int(str(a.get("player_hand")) == "L")
    row["b_is_lefty"] = int(str(b.get("player_hand")) == "L")
    row["same_hand_matchup"] = int(str(a.get("player_hand")) == str(b.get("player_hand")))
    row["rank_diff"] = row["a_player_rank"] - row["b_player_rank"]
    row["log_rank_diff"] = (
        log(row["a_player_rank"] + 1) - log(row["b_player_rank"] + 1)
        if not pd.isna(row["a_player_rank"]) and not pd.isna(row["b_player_rank"])
        else np.nan
    )
    row["elo_expected_a"] = expected_score(
        (1 - elo_config.surface_blend) * a["pre_overall_elo"]
        + elo_config.surface_blend * a["pre_surface_elo"],
        (1 - elo_config.surface_blend) * b["pre_overall_elo"]
        + elo_config.surface_blend * b["pre_surface_elo"],
    )
    row["fair_odds_elo_a"] = 1.0 / row["elo_expected_a"]
    row["fair_odds_elo_b"] = 1.0 / (1.0 - row["elo_expected_a"])
    return row


def _default_player_state():
    # Unfortunately we don't have elo_config easily accessible here without a closure.
    # But PlayerState() defaults to 1500 anyway, which matches initial_rating.
    return PlayerState()

def build_feature_tables(
    matches: pd.DataFrame | None = None,
    output_dir: Path = PROCESSED_DIR,
    elo_config: EloConfig | None = None,
    write: bool = True,
) -> dict[str, pd.DataFrame]:
    elo_config = elo_config or EloConfig()
    matches = load_matches() if matches is None else matches.copy()
    states: dict[int, PlayerState] = defaultdict(_default_player_state)
    snapshots: list[dict[str, Any]] = []
    history_rows: list[dict[str, Any]] = []
    training_rows: list[dict[str, Any]] = []
    elo_rows: list[dict[str, Any]] = []

    for _, date_matches in matches.groupby("tourney_date_dt", sort=True):
        pending_updates: list[tuple[pd.Series, dict[str, Any], dict[str, Any]]] = []
        for _, match in date_matches.iterrows():
            winner_id = int(match["winner_id"])
            loser_id = int(match["loser_id"])
            surface = match["surface"]
            winner_features = _state_features(
                states[winner_id],
                loser_id,
                match["loser_hand"],
                surface,
                match["tourney_date_dt"],
                elo_config,
            )
            loser_features = _state_features(
                states[loser_id],
                winner_id,
                match["winner_hand"],
                surface,
                match["tourney_date_dt"],
                elo_config,
            )
            winner_snapshot = _snapshot_row(match, "winner", winner_features)
            loser_snapshot = _snapshot_row(match, "loser", loser_features)
            snapshots.extend([winner_snapshot, loser_snapshot])
            history_rows.extend([_history_record(match, True), _history_record(match, False)])
            training_rows.append(
                _training_row(match, winner_snapshot, loser_snapshot, True, elo_config)
            )
            training_rows.append(
                _training_row(match, loser_snapshot, winner_snapshot, False, elo_config)
            )
            elo_rows.append(
                {
                    "match_id": match["match_id"],
                    "tourney_date": match["tourney_date"],
                    "surface": surface,
                    "winner_id": winner_id,
                    "loser_id": loser_id,
                    "winner_overall_elo_pre": winner_features["overall_elo"],
                    "loser_overall_elo_pre": loser_features["overall_elo"],
                    "winner_surface_elo_pre": winner_features["surface_elo"],
                    "loser_surface_elo_pre": loser_features["surface_elo"],
                }
            )
            pending_updates.append((match, winner_features, loser_features))

        for match, winner_features, loser_features in pending_updates:
            winner_id = int(match["winner_id"])
            loser_id = int(match["loser_id"])
            surface = match["surface"]
            tourney_level = match["tourney_level"]
            best_of = match.get("best_of", 3)
            sets_won = match.get("score_winner_sets_won", 2)
            sets_lost = match.get("score_loser_sets_won", 0)
            
            winner_state = states[winner_id]
            loser_state = states[loser_id]
            
            k_winner_overall = calculate_k_factor(winner_features["elo_matches_played"], tourney_level, best_of, sets_won, sets_lost)
            k_loser_overall = calculate_k_factor(loser_features["elo_matches_played"], tourney_level, best_of, sets_won, sets_lost)
            k_winner_surface = calculate_k_factor(winner_features["surface_elo_matches_played"], tourney_level, best_of, sets_won, sets_lost)
            k_loser_surface = calculate_k_factor(loser_features["surface_elo_matches_played"], tourney_level, best_of, sets_won, sets_lost)

            winner_state.overall_elo, loser_state.overall_elo = update_elo(
                winner_state.overall_elo, loser_state.overall_elo, 1.0, k_winner_overall, k_loser_overall
            )
            winner_state.surface_elo[surface], loser_state.surface_elo[surface] = update_elo(
                winner_state.surface_elo[surface],
                loser_state.surface_elo[surface],
                1.0,
                k_winner_surface,
                k_loser_surface,
            )
            winner_record = _history_record(match, True)
            loser_record = _history_record(match, False)
            winner_state.matches.append(winner_record)
            loser_state.matches.append(loser_record)
            winner_state.h2h[loser_id].append(winner_record)
            loser_state.h2h[winner_id].append(loser_record)

    matches_normalized = matches.copy()
    player_state_snapshots = pd.DataFrame(snapshots)
    player_match_history = pd.DataFrame(history_rows)
    model_training_rows = pd.DataFrame(training_rows)
    elo_history = pd.DataFrame(elo_rows)
    latest = []
    latest_date = matches["tourney_date_dt"].max()
    for player_id, state in states.items():
        latest.append(
            {
                "player_id": player_id,
                "state_as_of_date": latest_date,
                "overall_elo": state.overall_elo,
                **{f"{surface.lower()}_elo": state.surface_elo[surface] for surface in SURFACES},
                "matches_played": len(state.matches),
                "last_match_date": _last_date(state.matches),
            }
        )
    latest_player_state = pd.DataFrame(latest)

    tables = {
        "matches_normalized": matches_normalized,
        "player_match_history": player_match_history,
        "player_state_snapshots": player_state_snapshots,
        "model_training_rows": model_training_rows,
        "latest_player_state": latest_player_state,
        "elo_history": elo_history,
        "player_states_dict": states,
    }
    if write:
        ensure_output_dirs()
        output_dir.mkdir(parents=True, exist_ok=True)
        for name, table in tables.items():
            table.to_parquet(output_dir / f"{name}.parquet", index=False)
            
        import pickle
        with open(output_dir / "player_states.pkl", "wb") as f:
            pickle.dump(states, f)
            
    return tables

if __name__ == "__main__":
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent.parent
    # We must construct the match iterator.
    # Actually, better yet, the pipeline usually imports `build_feature_tables` and passes an iterator.
    # Let me check how it was run previously.
