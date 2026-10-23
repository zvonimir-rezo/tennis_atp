from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.frozen import FrozenEstimator
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from tennis_atp_pipeline.paths import MODELS_DIR, PROCESSED_DIR, REPORTS_DIR, ensure_output_dirs

TARGET = "player_a_wins"
CATEGORICAL_FEATURES = ["surface", "tourney_level", "round"]
NUMERIC_FEATURES = [
    "draw_size",
    "best_of",
    "rank_diff",
    "log_rank_diff",
    "diff_player_rank_points",
    "diff_player_age",
    "diff_pre_overall_elo",
    "diff_pre_surface_elo",
    "diff_pre_win_pct_last_10",
    "diff_pre_surface_win_pct_last_10",
    "diff_pre_fatigue_index_v1",
    "diff_pre_h2h_decayed_net",
    "diff_pre_win_pct_vs_hand",
    "diff_pre_service_points_won_pct",
    "diff_pre_return_points_won_pct",
    "diff_pre_service_games_won_pct",
    "diff_pre_return_games_won_pct",
    "diff_pre_win_after_winning_first_set_pct",
    "diff_pre_win_after_losing_first_set_pct",
    "diff_pre_days_since_last_match",
    "diff_pre_matches_last_7_days",
    "diff_pre_minutes_last_7_days",
    "diff_pre_retirements_last_10_matches",
    "a_is_lefty",
    "b_is_lefty",
    "same_hand_matchup",
    "elo_expected_a",
]


def load_training_rows(path: Path = PROCESSED_DIR / "model_training_rows.parquet") -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run `python -m tennis_atp_pipeline.build_features` first."
        )
    rows = pd.read_parquet(path)
    rows["tourney_date_dt"] = pd.to_datetime(rows["tourney_date_dt"])
    return rows


def _feature_columns(rows: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric = [col for col in NUMERIC_FEATURES if col in rows.columns]
    categorical = [col for col in CATEGORICAL_FEATURES if col in rows.columns]
    return numeric, categorical


def _preprocessor(rows: pd.DataFrame, scale_numeric: bool) -> ColumnTransformer:
    numeric, categorical = _feature_columns(rows)
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))
    return ColumnTransformer(
        transformers=[
            ("num", Pipeline(numeric_steps), numeric),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ],
        remainder="drop",
    )


def chronological_split(rows: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = rows[rows["tourney_date_dt"].dt.year <= 2023].copy()
    validation = rows[rows["tourney_date_dt"].dt.year == 2024].copy()
    test = rows[rows["tourney_date_dt"].dt.year == 2025].copy()
    if train.empty or validation.empty or test.empty:
        raise ValueError("Expected non-empty train<=2023, validation=2024, and test=2025 splits.")
    return train, validation, test


def _evaluate(model: Pipeline, rows: pd.DataFrame, label: str) -> dict[str, float | str | int]:
    numeric, categorical = _feature_columns(rows)
    x = rows[numeric + categorical]
    y = rows[TARGET].astype(int)
    p = model.predict_proba(x)[:, 1]
    return {
        "split": label,
        "rows": int(len(rows)),
        "log_loss": float(log_loss(y, p)),
        "brier": float(brier_score_loss(y, p)),
        "auc": float(roc_auc_score(y, p)),
        "accuracy": float(accuracy_score(y, p >= 0.5)),
    }


def train_models(
    rows: pd.DataFrame | None = None,
    model_dir: Path = MODELS_DIR,
    report_dir: Path = REPORTS_DIR,
) -> dict[str, object]:
    ensure_output_dirs()
    rows = load_training_rows() if rows is None else rows.copy()
    rows = rows.dropna(subset=[TARGET, "tourney_date_dt"])
    train, validation, test = chronological_split(rows)
    numeric, categorical = _feature_columns(rows)

    logistic = Pipeline(
        [
            ("preprocess", _preprocessor(rows, scale_numeric=True)),
            ("model", LogisticRegression(max_iter=2000)),
        ]
    )
    logistic.fit(train[numeric + categorical], train[TARGET].astype(int))

    base_gb = Pipeline(
        [
            ("preprocess", _preprocessor(rows, scale_numeric=False)),
            (
                "model",
                HistGradientBoostingClassifier(max_iter=250, learning_rate=0.05, random_state=7),
            ),
        ]
    )
    base_gb.fit(train[numeric + categorical], train[TARGET].astype(int))
    calibrated_gb = CalibratedClassifierCV(FrozenEstimator(base_gb), method="isotonic")
    calibrated_gb.fit(validation[numeric + categorical], validation[TARGET].astype(int))

    metrics = [
        {"model": "logistic", **_evaluate(logistic, validation, "validation_2024")},
        {"model": "logistic", **_evaluate(logistic, test, "test_2025")},
        {
            "model": "calibrated_gradient_boosting",
            **_evaluate(calibrated_gb, validation, "validation_2024"),
        },
        {"model": "calibrated_gradient_boosting", **_evaluate(calibrated_gb, test, "test_2025")},
    ]
    model_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(logistic, model_dir / "baseline_logistic.joblib")
    joblib.dump(calibrated_gb, model_dir / "calibrated_model.joblib")
    metadata = {
        "numeric_features": numeric,
        "categorical_features": categorical,
        "target": TARGET,
        "train_rows": int(len(train)),
        "validation_rows": int(len(validation)),
        "test_rows": int(len(test)),
    }
    (model_dir / "feature_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    pd.DataFrame(metrics).to_csv(report_dir / "model_metrics.csv", index=False)
    return {
        "logistic": logistic,
        "calibrated_model": calibrated_gb,
        "metrics": metrics,
        "metadata": metadata,
    }


def main() -> None:
    result = train_models()
    print(pd.DataFrame(result["metrics"]).to_string(index=False))


if __name__ == "__main__":
    main()
