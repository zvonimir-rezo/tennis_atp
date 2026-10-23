from __future__ import annotations

from pathlib import Path

import pandas as pd

from tennis_atp_pipeline.paths import DEFAULT_YEARS, PROJECT_ROOT
from tennis_atp_pipeline.score import parse_score


def _to_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def load_players(root: Path = PROJECT_ROOT) -> pd.DataFrame:
    players = pd.read_csv(root / "atp_players.csv")
    players["player_id"] = pd.to_numeric(players["player_id"], errors="coerce").astype("Int64")
    return players


def load_rankings(root: Path = PROJECT_ROOT) -> pd.DataFrame:
    files = [
        root / "atp_rankings_10s.csv",
        root / "atp_rankings_20s.csv",
        root / "atp_rankings_current.csv",
    ]
    rankings = [pd.read_csv(path) for path in files if path.exists()]
    if not rankings:
        return pd.DataFrame(columns=["ranking_date", "rank", "player", "points"])
    df = pd.concat(rankings, ignore_index=True).drop_duplicates()
    df = _to_numeric(df, ["ranking_date", "rank", "player", "points"])
    df["ranking_date_dt"] = pd.to_datetime(df["ranking_date"], format="%Y%m%d", errors="coerce")
    return df.sort_values(["ranking_date", "rank", "player"]).reset_index(drop=True)


def load_matches(years: tuple[int, ...] = DEFAULT_YEARS, root: Path = PROJECT_ROOT) -> pd.DataFrame:
    frames = []
    for year in years:
        path = root / f"atp_matches_{year}.csv"
        if path.exists():
            frame = pd.read_csv(path)
            frame["source_year"] = year
            frames.append(frame)
    if not frames:
        raise FileNotFoundError("No atp_matches_{year}.csv files found for requested years.")

    matches = pd.concat(frames, ignore_index=True)
    return normalize_matches(matches)


def normalize_matches(matches: pd.DataFrame) -> pd.DataFrame:
    matches = matches.copy()
    numeric_columns = [
        "draw_size",
        "tourney_date",
        "match_num",
        "winner_id",
        "winner_seed",
        "winner_ht",
        "winner_age",
        "loser_id",
        "loser_seed",
        "loser_ht",
        "loser_age",
        "best_of",
        "minutes",
        "w_ace",
        "w_df",
        "w_svpt",
        "w_1stIn",
        "w_1stWon",
        "w_2ndWon",
        "w_SvGms",
        "w_bpSaved",
        "w_bpFaced",
        "l_ace",
        "l_df",
        "l_svpt",
        "l_1stIn",
        "l_1stWon",
        "l_2ndWon",
        "l_SvGms",
        "l_bpSaved",
        "l_bpFaced",
        "winner_rank",
        "winner_rank_points",
        "loser_rank",
        "loser_rank_points",
    ]
    matches = _to_numeric(matches, numeric_columns)
    matches["tourney_date_dt"] = pd.to_datetime(
        matches["tourney_date"].astype("Int64").astype(str), format="%Y%m%d", errors="coerce"
    )
    matches["match_id"] = (
        matches["tourney_id"].astype(str)
        + "_"
        + matches["match_num"].astype("Int64").astype(str)
        + "_"
        + matches["winner_id"].astype("Int64").astype(str)
        + "_"
        + matches["loser_id"].astype("Int64").astype(str)
    )
    parsed = matches["score"].apply(parse_score).apply(pd.Series)
    matches = pd.concat([matches, parsed.add_prefix("score_")], axis=1)
    matches["is_retirement"] = (
        matches["score"].fillna("").str.contains("RET", case=False, regex=False)
    )
    matches["surface"] = matches["surface"].fillna("Unknown")
    return matches.sort_values(["tourney_date_dt", "tourney_id", "match_num"]).reset_index(
        drop=True
    )
