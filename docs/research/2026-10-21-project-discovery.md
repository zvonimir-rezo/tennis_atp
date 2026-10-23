# ATP direction discovery: implementation, evidence and decision

Investigated 2026-10-21. **Provisional recommendation: a small collection of interactive tennis match investigations.** The choice remains open until the builder interview. Its strongest evidence is one fully recoverable scoring paradox, an accessible point-level source, and a clear interaction difference from the inspected statistics tables. Enjoyment, novelty and repeat use are hypotheses.

Companion: [external evidence and sources](2026-10-21-external-discovery.md). Task/checkpoint: [discovery-task.md](discovery-task.md). Nothing was published or integrated; production source and upstream CSVs were not changed.

## What actually works

The current checkout is upstream commit `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0` plus pre-existing, untracked application code/docs and many pre-existing upstream file deletions. A clone of that commit alone cannot reproduce the application. No existing task record, test directory or dependency lock was found.

I installed disposable dependencies outside the repository and ran the existing CLI and `gui_server.py`. The rendered interface at `http://127.0.0.1:8080/` accepts two names, a surface and optional decimal odds. It returns percentages, fair odds and a quarter-Kelly suggestion. Its autocomplete is a precomputed player list, including historical players. It has no historical match picker, source evidence, explanation, freshness display or probability interval.

Observed browser run: Carlos Alcaraz vs Jannik Sinner, Clay, entered illustrative odds 2.50/1.60 → **41.7% / 58.3%, fair odds 2.40 / 1.72**, with “Profitable Edge Found”, +4.3% EV and 0.71% of bankroll. These are calculations from the model and invented test prices, **not an observed opportunity or validated profitable strategy**. The run's wall-clock date is 2026-10-21.

There are two prediction paths:

- The GUI imports root `predict.py` and loads `models/logreg_model.pkl` plus pickled player states. `train_final_model.py` fits all eligible years, including 2025 and partial 2026, and calibrates with ordinary five-fold CV. This artifact cannot be evaluated as an untouched 2025 forecast model.
- `src/tennis_atp_pipeline/train.py` fits through 2023, calibrates boosted trees on 2024, and evaluates 2025. Its `price_match` path uses different saved models. The saved metrics/metadata refer to an older set of rows (2025: 5,724 mirrored rows versus the current 5,888). The GUI does not serve this model.

I rebuilt features **in memory using the existing implementation**: 51,802 mirrored rows for 25,901 matches. Saved and rebuilt Elo probability, surface-Elo difference, fatigue difference and rolling service-points difference matched exactly, including missing values. This verifies those selected features and row linkage, not every possible feature invariant. The monolithic `update.sh` was not run: its expected `.venv` is absent and it overwrites existing artifacts. Existing inference, feature generation and a temporal model fit were exercised independently without replacing those artifacts.

## A real match traced end to end

Local source: `atp_matches_2025.csv`, `tourney_id=2025-520`, `match_num=401`, Alcaraz (207989) over Sinner (206173), Roland Garros final. Score: `4-6 6-7(4) 6-4 7-6(3) 7-6(2)`, 329 minutes. The deterministic normalized match ID is `2025-520_401_207989_206173`.

1. **Source semantics:** the local row says `tourney_date=20250526`, not June 8, the actual final date. Rankings are 2 versus 1, points 8,850 versus 10,380.
2. **Historical state:** features are frozen before the entire May 26 tournament-date batch. Alcaraz overall/surface Elo = 2095.84/2080.35; Sinner = 2194.88/1930.71. Recorded histories contain 300/366 prior ATP matches since 2017. Both last-ten win rates = 90%. Both show 19 “days since last match” and zero matches/minutes in the last seven days.
3. **Why the zero matters:** the source also contains Alcaraz's six earlier rounds in the same tournament. They are deliberately withheld from the final's features because all seven rounds share one date. Their minutes are missing in this local source. These are conservative tournament-start estimates, not final-day fatigue measurements.
4. **Temporal forecast:** fitting <=2023, calibrating on 2024 and scoring the 2025 row yields Alcaraz **53.10%**, fair odds about **1.88**. Blended Elo gives **53.63%**; rank/points-only logistic gives **41.63%**. This illustrates a surface-versus-ranking disagreement; it is not proof of why he won.
5. **Actual deployed artifact:** applying the GUI's all-years artifact to that historical feature row yields **53.77%**. That value has training contamination for retrospective evaluation and is not admissible evidence of forecasting success.
6. **User experience:** entering the same players and Clay in the GUI produces today's hypothetical matchup, **41.7%**, because it uses latest saved states and wall-clock ages/rest. It cannot replay the historical 53.1% estimate. Training uses blended Elo for `elo_expected_a`; the GUI supplies overall-only Elo under that same feature name. The trace therefore exposes a real training/inference mismatch, not one continuous historical replay experience.

The outcome record itself offers a better product hook than a small prediction edge: Alcaraz won **192 total points to Sinner's 193**. Formula from the ATP row: Alcaraz serve points won 71+46=117, return points won 191−72−44=75; total 192 of 385. The independently accessible charted point sequence recovers all 385 points and the three saved championship points. [Official Roland Garros corroboration](https://www.rolandgarros.com/en-us/article/rg2025-rg-live---day-15-sunday-8-june), [actual Tennis Abstract report](https://www.tennisabstract.com/charting/20250608-M-Roland_Garros-F-Jannik_Sinner-Carlos_Alcaraz.html).

## Material constraints

| Constraint | Observed evidence | Consequence |
|---|---|---|
| Scope | 25,901 matches; 1,172 distinct players; 2017–2025 plus 1,169 partial-2026 rows. Davis Cup/team events are present. Older, qualifying and Challenger files are absent locally. | “Career” means observed since 2017. Lower-tour development and all-time records are unsupported. |
| Freshness | Maximum tournament date April 22, 2026. Current-ranking file spans Jan 5–May 4. GUI takes the first matching ranking row: Alcaraz 12,050 vs Sinner 11,500 points from Jan 5, despite May 4 values 12,960/14,350. | Current inference silently mixes stale periods. A historical edition has much lower operational burden. |
| Granularity | Box scores and set scores; no point sequence, shot placement, tracking, injury feed or actual match timestamp in ATP base files. | Do not infer tactical mechanisms, precise rest or injury probabilities from these alone. |
| Missingness | Minutes absent 6.33%; serve-point totals 4.34%; winner/loser ranks absent 0.47%/1.33%. 53 surfaces normalized to Unknown, eight Carpet. | Base source is broad but not uniformly complete. Raw completeness understates derived feature missingness. |
| Rolling missingness | About 30.12% of player snapshots lack rolling service-points win rate. `_rate` includes NaNs in its mean; a missing match can contaminate a 20-match window. | A generic automated explanation may present imputation as evidence. Coverage/sample counts must be visible in any analytical experience. |
| Time and leakage | Date-batch snapshots exclude same-tournament rounds, avoiding current-outcome leakage but discarding useful prior rounds. Prior-event updates are applied in match-number order after the batch. | Valid tournament-cutoff baseline; not a faithful continuous match-day state. Two-week events and overlapping dates limit temporal certainty further. |
| Targets | 675 RET, 162 W/O, five DEF and one ABD in source; 324 mirrored W/O rows are included. Retirement flag applies to both players' history records. | Largest errors can reflect injury/non-play. “Mental resilience” and “psychological edge” labels in docs are interpretations, not measured mechanisms. |
| Reproducibility | No `.venv`/lock/tests; lower-bound sklearn dependency permits versions without `FrozenEstimator`; saved artifacts identify sklearn 1.8.0. Setup instructions say Python3.10, pyproject requires >=3.11. | Pin an edition/runtime before presenting a finished demonstration; no broad cleanup is needed to choose a direction. |
| Access | Original ATP upstream returns 404; cause/permanence unknown. Public Match Charting Project downloads work, without account/key; download freshness lags live site. | Do not promise automatic current-season coverage. A pinned, attributed archive is feasible now. |
| Terms | Local ATP README and original MCP README specify CC BY-NC-SA4.0. [Official deed](https://creativecommons.org/licenses/by-nc-sa/4.0/) requires credit, noncommercial use and same-license sharing of adaptations. | Retain provenance/license for data and adaptations. Commercialization is a separate unresolved direction. Public access does not confer video rights. |
| Odds | Local Parquet has 2017–May2026 Excel filenames but no verified fetch/quote provenance. Original provider returned403. Rank-first join permits different players/events. | No defensible market edge or ROI claim. Specific wrong join: Paris2025 Sinner–Shelton linked to Vienna Sinner–De Minaur. |

## Probability audit

A disposable evaluation reused the rebuilt feature definitions and fixed C=0.1 (already selected in the project). Train: 12,463 eligible matches through2023; sigmoid calibration: 2,410 in2024; evaluation: **2,179 in2025**, requiring both players to have >=20 prior matches. This excludes 765 of the2,944 raw2025 matches, so results do not describe cold-start players. Mirrored training rows are not counted as independent test matches; evaluation uses one deterministic player-ID orientation per match.

| Model | 2025 log loss ↓ | Brier ↓ | Accuracy |
|---|---:|---:|---:|
| Coin probability | .69315 | .25000 | Tie choice is arbitrary |
| Rank/points logistic | .62588 | .21883 |64.48%|
| Overall/surface Elo | .62388 | .21809 |63.79%|
| 19-feature logistic + sigmoid | **.61115** | **.21257** |66.09%|

Removing RET/W/O/DEF/ABD test rows leaves2,067 matches: log loss .60444 model, .61458 Elo and .62189 rank. A paired bootstrap over tournament-date groups gives model improvement over Elo .01273, descriptive95% interval [.00602,.01960]; over rank .01473 [.00615,.02395]. These intervals do not account for tuning, previous test inspection, or independent future seasons.

Calibration is plausible, not perfect: of638 predictions with a60–70% favorite, mean forecast64.68%, observed win fraction66.93%; at70–80%, 383matches,74.32% forecast versus71.80% observed. Only81 matches have >=90% favorites. Brier/log loss combine discrimination and reliability; they do not by themselves prove calibration. [scikit-learn calibration documentation](https://scikit-learn.org/1.8/modules/calibration.html).

**Interpretation:** enough signal for a transparent experimental benchmark; no superiority to licensed, correctly timestamped bookmaker prices has been established.2025 has already been inspected in project notebooks, so this is a reproducibility/sensitivity audit, not a fresh blind test. Notebook tuning uses year folds that also train on later years within the pre2024 pool. Its ROI chart selects the best edge threshold on2025 and counts mirrored rows twice. GUI final-model CV likewise trains on future years relative to held-out blocks. [Temporal validation reference](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html).

## Errors and anomalies as product evidence

- **Goffin over Alcaraz, Miami2025:** temporal model gives the eventual winner7.60%, rank15.53%, Elo8.85%; actual score5–7 6–4 6–3. A useful judgment-game example: an unlikely outcome is compatible with a reasonable probability. No feature attribution establishes a hidden cause.
- **Griekspoor over Sinner, Shanghai2025:**3.60% for the winner, score6–7(3) 7–5 3–2 RET. The worst error is partly a target/availability issue, not automatically a lesson about tactical strength.
- **Bergs over Rublev, Miami2025:** apparent44.37% point-win fraction looks even more surprising than the RGfinal. But break totals contradict the completed straight-set score. Reject it as a tennis “fact” until independently repaired. A data anomaly scanner is not a story generator.
- **RGfinal:** point totals agree across local boxscore,385 charted points and official report. This survives the verification that the Bergs example fails.

## Adjacent products inspected

I opened the actual Tennis Abstract RGfinal page and switched from Stats Overview to Point-by-point description. It exposes the result immediately and offers dozens of tables plus a long chronological text list. The proposed case-file distinction is one guided question, a small sequence of evidence reveals and an explicit conclusion, not possession of these statistics. Tennis Abstract already lists minority-point winners in its Lottery Matches report: the paradox itself is not original.

I opened RallyIQ's rendered homepage, with two-player game-plan form, scouting form and example links. Its Alcaraz–Sinner matchup link hit a security challenge; no generated plan was verified. Generic tactical profiles have direct adjacent competition.

I opened the actual Dimitrov–Monfils TennisTV replay page: premium subscription gate, library/watchlist navigation and “Play Predictor & Polls” already exist. Playback and logged-in spoiler mode were not tested. A protected video is not an available distributable asset. The external note records firsthand viewers asking which match to watch and having a partner start playback to avoid duration spoilers. These are concrete behaviors from self-selected anecdotes, not measured demand.

## Three genuinely different directions

### A. Match investigations — provisional recommendation

**Experience and return:** a tennis-curious viewer starts with a paradox, makes a judgment, scrubs/reveals a few decisive pieces of evidence and leaves able to explain what happened. Return would be for another short authored investigation, including matches they already know.

**Real example:** “Alcaraz won fewer points. Where did the match go?” Toggle the same385points between cumulative totals and tennis score; inspect the three championship points, then the final tiebreak. Clearly separate recorded scoring facts from any modeled leverage. Do not claim he caused the victory through “clutch mentality.”

**Distinctive relative to inspected products:** Tennis Abstract supplies detailed tables and a point list; this would provide a deliberately paced, answerable question with provenance and a satisfying reveal. Counts/paradoxes are already available. Whether the interaction feels new is untested.

**Smallest complete version:** two authored cases, a shared reveal/scrub interaction, clear source/cutoff panel and a deliberate ending. One verified point-level case plus a contrasting aggregate-data case is enough. No universal explorer, video synchronization, generated tactical advice or live predictions.

**Hardest assumption/burden/rejection:** the explanation must feel better than reading a chart or watching highlights. Source verification and writing are the recurring work; the engineering can become mostly finished. Reject if the builder dislikes editorial curation or the visitor only wants footage.

**Portfolio demonstration:** visual interaction design, score-state/domain modeling, data integration, reproducible provenance, careful inference and a finished narrative. It demonstrates less ongoing ML research than directionB.

**Cheapest observable test:** prepare two rough reveal sequences before building a site. Observe five tennis viewers. Support if >=3 voluntarily open case2 and >=4 can correctly explain case1 without being prompted with the answer. Do not send invitations without authorization. Failure means rethink the central interaction, not add a dashboard. Test whether authoring the second case remains enjoyable for the builder.

### B. Forecast judgment game

**Experience and return:** tennis followers estimate a probability from a historical pre-tournament dossier, lock it, inspect rank/Elo/model benchmarks, then reveal the result. The continuing object is their own calibration, not a betting balance or a leaderboard based on lucky winner picks.

**Real example:** Goffin–Alcaraz Miami2025. Show only the pre-tournament rankings/surface/form, collect confidence, reveal Goffin's three-set win and the model's7.6% probability. One upset should not imply the participant or model is wrong; score across an ordinary-match set with a proper probability score.

**Distinctive:** TennisTV already offers predictor/polls, and Tennis Abstract forecasts. This is a closed learning loop about confidence, explicitly comparing simple models and acknowledging remembered results. Outcome memory is a central weakness, not a solved UX detail.

**Smallest complete version:**20 fixed historical matches, one consistent cutoff, probability input, reveal, cumulative Brier score and a readable personal calibration summary. Include ordinary matches and losses, not a deck selected only for upsets. No accounts, money, live feed, model zoo or strategy advice.

**Hardest assumption/burden/rejection:** known results contaminate judgment; hiding names may remove tennis attachment. Historical features and benchmark versions need careful curation; maintenance can be periodic for a pinned edition. Reject if obscure matches feel like arbitrary trivia or honest uncertainty feels unsatisfying to the builder.

**Portfolio demonstration:** temporal ML evaluation, calibration, proper scoring, experiments and game interaction design. The differentiator is the teaching/learning experience, not a claim to beat markets.

**Cheapest observable test:** ten paper/form cards with a probability scale; then make a second set available without prompting. Support if >=3/5 unfamiliar-result participants voluntarily continue and can explain why a70% estimate losing once need not be a bad estimate. Record known-result contamination; if >20% of cards are remembered, change the sampling premise before building. Improvement in calibration needs many more observations than this appeal test.

### C. Spoiler-free replay curator

**Experience and return:** a replay watcher describes the kind of tennis evening they want and gets one concealed recommendation with a short, spoiler-safe reason. Return is at their next watch session, not to browse more stats.

**Real example:** Dimitrov–Monfils, IndianWells2025 R3. Local record, chart and official TennisTV replay all exist; firsthand viewers recommended this exact match. The local181minutes and three-set score are for curation, not display before playback. RGfinal is not a TennisTV replay candidate because that service excludes Slams.

**Distinctive:** TennisTV already hides scores/timeline; NoSpoilerTennis has offered spoiler-aware lists. The proposed value is making the selection itself easier while concealing outcome clues. That advantage is unproven and weaker thanA's portfolio distinction.

**Smallest complete version:** six hand-checked replays in one provider/region context, three mood choices, one recommendation at a time, neutral link handoff and post-watch feedback. Avoid exact duration, score, winner thumbnails and promises of universally spoiler-free provider pages. No video hosting, account integration or automatic whole-tour excitement ranking.

**Hardest assumption/burden/rejection:** a recommendation must select enjoyable tennis rather than merely a close score. Subscription, region, link availability and provider spoilers remain outside the curator's control. Link checks and editorial watching continue; reject if usefulness depends on controlling protected playback or the builder does not watch replays.

**Portfolio demonstration:** restrained UX, preference/recommendation design and behavioral testing; less strong evidence of modeling depth. External handoff weakens the self-contained finished experience.

**Cheapest observable test:** give five existing replay watchers three concealed, playable options versus their ordinary selection method; record actual starts and post-watch fit, then observe a second session. Support if >=3 select and start an available recommendation and >=2 return voluntarily within a week. The test must include availability failures. This is a small falsification screen, not demand validation.

## Recommendation and pending interview

Start by testingA. It has a verified complete example, can be a deliberately finished historical edition and puts the central interaction ahead of data freshness. Exclude betting/ROI, live touring coverage, generalized tactical prescriptions, comprehensive player profiles and automatic video alignment from that provisional experiment.

Do not commit toA because it sounds impressive. Its central builder risk is that the enjoyable engineering runs out and the work becomes editorial production. B is preferable if repeated model experiments and designing honest feedback are the satisfying part. C deserves consideration if the builder already watches replays and has a personal selection problem; usefulness alone is a weak reason given the stated priorities.

Interview tree, one question per turn:
1. Choose the kind of difficult work the builder wants to return to: authored visual explanations, probability/game experiments, or replay curation.
2. Resolve that branch's actual central interaction and hardest assumption; challenge generic “all sound good.”
3. Establish the portfolio moment and the maintenance bargain (finished edition vs recurring service).
4. Agree one exclusion set and a small observable test with a success/failure rule.
5. Confirm shared direction and record it. No large roadmap; do not silently choose for the user.

## Reproduction and artifacts

Disposable runtime: `/private/tmp/atp-discovery-313/bin/python`, Python3.13.7, pandas2.2.3, numpy2.5.4, sklearn1.8.0, pyarrow26.0.0, joblib1.6.0. Standard system Python lacked packages; a Python3.14 source-build attempt failed; Python3.13 binary wheels worked. No project dependency file was edited.

From repository root:

```sh
PYTHONPATH=src:. /private/tmp/atp-discovery-313/bin/python docs/research/discovery_probe.py
PYTHONPATH=src:. /private/tmp/atp-discovery-313/bin/python docs/research/forecast_sensitivity.py
PYTHONPATH=src:. /private/tmp/atp-discovery-313/bin/python docs/research/odds_probe.py
```

Outputs are ignored under `reports/discovery/`: input SHA256s, coverage, selected rebuild comparison, independent-match evaluation/calibration bins, completed-match sensitivity/bootstrap, trace JSON, upset rows, suspect odds links, copied raw RGpoint subset and execution log. The scripts are disposable investigation aids, not proposed production architecture. The odds probe intentionally flags only conspicuous name disagreements; transliterations remain false positives and it is not a complete join audit.
