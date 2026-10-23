# Feature Importance — Logistic Regression Model

> **19 player-specific features only.** Non-player features (`surface`, `tourney_level`, `round`, `draw_size`, `best_of`) were removed — they had near-zero coefficients and carry no information about individual player quality.  
> **Best C = 0.1** (strong L2 regularisation).  
> All `diff_` features = `player_A_value − player_B_value`. Positive coefficient → favours player A winning.

---

## Features Ranked by Coefficient Magnitude

| Rank | Feature | Coef | What it measures |
|------|---------|------|-----------------|
| 1 | `diff_pre_surface_elo` | +0.605 | Career Elo on this specific surface (Clay / Hard / Grass). Strongest signal — captures surface specialisation built over an entire career. |
| 2 | `diff_pre_overall_elo` | +0.461 | Overall career Elo across all surfaces. General skill gap between players. |
| 3 | `elo_expected_a` | −0.286 | Raw Elo win probability for player A (0–1). Negative because once the two Elo diffs above are included, this dampens overconfidence in extreme mismatches. |
| 4 | `diff_pre_fatigue_index_v1` | −0.173 | Composite fatigue score: matches + minutes played in last 7 days, rest days, recent SF/Final appearances. More fatigued player A → lower win prob. |
| 5 | `diff_player_age` | −0.159 | Age difference. Older player A is modestly disadvantaged — reflects the ATP peak performance curve (~25–28). |
| 6 | `diff_player_rank_points` | +0.149 | ATP ranking points difference. 52-week rolling window — captures consistency and quality of results over a full season. |
| 7 | `diff_pre_matches_last_7_days` | +0.116 | Matches played in the last 7 days. More matches = deeper in a tournament = in-form signal. |
| 8 | `diff_pre_days_since_last_match` | −0.088 | Days since last match. More rest for player A slightly hurts — proxy for having lost earlier in a previous event. |
| 9 | `diff_pre_return_points_won_pct` | +0.078 | Rolling return points won % (last ~20 matches with point data). One of the most predictive stats in pro tennis. |
| 10 | `diff_pre_minutes_last_7_days` | +0.075 | Total match minutes in last 7 days. Complements #7 — more match time = deeper in tournament. The fatigue index handles the negative side. |
| 11 | `diff_pre_win_after_winning_first_set_pct` | −0.070 | Close-out rate when winning first set. Slight negative — historically correlated with facing weaker opponents, already priced into Elo. |
| 12 | `diff_pre_win_pct_last_10` | +0.067 | Win % across last 10 matches. Recent form signal — captures hot/cold streaks not yet reflected in Elo. |
| 13 | `diff_pre_service_points_won_pct` | +0.065 | Rolling serve points won %. Complements return efficiency (#9). |
| 14 | `diff_pre_surface_win_pct_last_10` | −0.049 | Win % on this surface over last 10 matches. Slight negative — surface Elo (#1) captures this more robustly; last-10 on surface is noisy. |
| 15 | `diff_pre_h2h_decayed_net` | +0.046 | Time-decayed head-to-head net wins. Captures psychological edge in recurring matchups. |
| 16 | `diff_pre_retirements_last_10_matches` | −0.033 | Retirement rate in last 10 matches. Injury risk / physical condition proxy. |
| 17 | `diff_pre_win_after_losing_first_set_pct` | −0.025 | Win rate when losing first set. Mental resilience — small signal, overshadowed by Elo. |
| 18 | `a_is_lefty` | −0.023 | Player A is left-handed. Tiny effect — mostly absorbed into serve/return stats. |
| 19 | `b_is_lefty` | +0.023 | Player B is left-handed. Mirror of #18. |

---

## Removed Features (and why)

| Feature | Reason removed |
|---------|---------------|
| `surface`, `tourney_level`, `round` | Match/tournament properties — not player-specific. Near-zero coefficients. |
| `draw_size`, `best_of` | Tournament structure — not player-specific. |
| `same_hand_matchup` | Near-zero interaction term. |
| `log_rank_diff` | Redundant — fully collinear with `diff_player_rank_points`. |
| `diff_pre_win_pct_vs_hand` | Coefficient ~0.002. No useful signal. |
| `diff_pre_service_games_won_pct` | Collinear with `diff_pre_service_points_won_pct`. |
| `diff_pre_return_games_won_pct` | Collinear with `diff_pre_return_points_won_pct`. |

---

## Model Performance (Test 2025)

| Model | Log Loss | AUC | Accuracy |
|-------|----------|-----|----------|
| Elo baseline | 0.6239 | 0.707 | 63.8% |
| **LogReg – 19 features** | **0.6111** | **0.720** | **66.1%** |
| Bookmaker ceiling | ~0.595 | — | — |

Removing 10 non-informative features had **zero negative impact** on performance — confirming the pruning was correct.
