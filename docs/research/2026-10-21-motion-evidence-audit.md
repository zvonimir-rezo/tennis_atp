# Margins: independent evidence audit for motion planning

2026-10-21. Planning only: no UI, dependencies, source-data edits or model changes. Re-read the agreed direction and existing case audit; independently recounted the retained point records and replayed scoring rather than calling the existing probe.

## What can carry the argument

**Claim:** Federer's 14-point advantage was real and concentrated; the full-match total alone does not establish sustained dominance. This is a descriptive claim about the distribution of recorded points, not a measure of overall playing quality.

| Partition | Record IDs (`Pt`, inclusive) | n | Federer | Djokovic | Federer margin |
|---|---|---:|---:|---:|---:|
| Full match | 1–422 | 422 | 218 | 204 | +14 |
| Set 1 | 1–87 | 87 | 41 | 46 | −5 |
| Set 2 | 88–125 | 38 | 26 | 12 | +14 |
| Set 3 | 126–198 | 73 | 37 | 36 | +1 |
| Set 4 | 199–253 | 55 | 30 | 25 | +5 |
| Set 5 | 254–422 | 169 | 84 | 85 | −1 |
| Other four sets | all except 88–125 | 384 | 192 | 192 | 0 |
| Three tiebreaks | 76–87; 188–198; 413–422 | 33 | 12 | 21 | −9 |
| Other four sets, excluding tiebreaks | complement of set 2 and three tiebreaks | 351 | 180 | 171 | +9 |

Thus a disjoint decomposition is **38 + 33 + 351 = 422 points**, with margins **+14 − 9 + 9 = +14**. It avoids double counting and qualifies a superficial “the other four sets were even”: their aggregate was even, but neither their individual sets nor their tiebreak/non-tiebreak partitions were equal. Use the complete ledger as context, not a story in which the second set vanishes.

**Strongest objection:** Set two counted. Federer really won it decisively; discarding it is selective if presented as a fairer assessment of the match. Further, equal point totals across four sets do not establish equal quality, equal opportunity, equal serve/return performance or equal performance at each score state. Answer the objection by showing a partition of the same history and explicitly limiting the verdict. Do not infer that the later match would have played identically without set two. Do not infer intent, nerves, choking, tactical causation or championship deservedness.

**Not original research:** [Schewior's July 2019 commentary](https://www.deconstructingtennis.com/blog/wimbledon-mens-final-analysis-2019/) already stated the 192–192 result. [Sackmann's July 2019 analysis](https://www.tennisabstract.com/blog/2019/07/26/roger-federer-wasnt-clutch-but-he-was-almost-clutch-enough/) already considered modeled leverage and warned against judging Federer's overall high-leverage play only by famous failures. Its modeled values were not reproduced here. Tiebreak membership is not a synonym for all important points.

## Actual score states and definitions

The retained original-format CSV subset is `reports/discovery/wimbledon2019-final-points.json`, match `20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic`, SHA-256 `b772afeb9e76baa3f0c7c21c0351ae72dddfcf47afe2111378b6bfeb720e89f3`. Identity is `(match_id, Pt)`, not drawing position. All 422 identities are unique and `Pt` is exactly 1–422. Source attribution is MCP / Tennis Abstract, charted by Zindaras, as confirmed by the [actual match report](https://www.tennisabstract.com/charting/20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic.html).

The [MCP dictionary](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/data_dictionary.txt) defines player 1 as the first server (Federer here), `Set1/Set2` and `Gm1/Gm2` as completed sets/games, `Svr` as server identity and `PtWinner` as winner identity. `TbSet` describes whether a set permits a tiebreak; **it is not point-level tiebreak membership**. This older specimen has no `TB?` column. The [MCP README](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/README.md) explains that `1st`, `2nd`, `Notes` are contributor input; derived score/winner fields are generated. Do not call generated fields independently observed measurements.

**Important discovered convention:** `Pts` is pre-point and server-relative in this specimen. The dictionary says only “point score”; independently replaying every point establishes orientation here. At point 81, Djokovic serves and `Pts=3-2`, meaning Djokovic 3, Federer 2. A UI with stable Federer/Djokovic left/right order must normalize the score by `Svr`; copying `Pts` into that layout silently reverses scores as service changes.

Scoring replay, initialized 0–0 sets/games/points with Federer serving, matched **all 422 pre-point `Set1`, `Set2`, `Gm1`, `Gm2`, `Pts`, `Svr`, `Gm#` values**. Ordinary games use four points with a two-point lead; ordinary sets six games with a two-game lead. Tiebreaks occur at 6–6 in sets 1–4, **12–12 in set 5**, target seven with a two-point lead. Tiebreak service is one point then alternating blocks of two; the following set's first server reverses the tiebreak's first server. Replay ends Federer 2 sets, Djokovic 3, with set game scores 6–7, 6–1, 6–7, 6–4, 12–13. The [official Wimbledon result sheet](https://www.wimbledon.com/en_GB/scores/2019/schedule/pdf/schedulePDF21.pdf) independently confirms that final result; the [ITF contemporaneous account](https://www.itftennis.com/en/news-and-media/articles/djokovic-beats-federer-in-epic-wimbledon-final/) confirms the 12–12 breaker and championship points.

| Record | Pre-point state | Server | Point winner | Literal charting |
|---|---|---|---|---|
| 359 | 2–2 sets; Federer 8–7; 40–15 | Federer | Djokovic | first `6n`; second `4f28f3w@` |
| 360 | 2–2 sets; Federer 8–7; 40–30 | Federer | Djokovic | first `6r28f+1f1*`; no second |

Both are championship points **for Federer**, and neither is in a tiebreak. The [charting quick-start](https://www.tennisabstract.com/blog/2015/09/23/the-match-charting-project-quick-start-guide/) explains serve/shot/error and approach symbols. These encode recorded actions and outcomes; they do not establish why a player chose them. No actual-time timestamps, coordinates or frame-accurate trajectory are present. A timeline must be point ordinal, not fabricated elapsed time.

## Independence and access limits

Local `atp_matches_2019.csv`, row `2019-540 / 226`, separately yields Djokovic 204 points: 101 first-serve wins + 39 second-serve wins + (203 Federer service points − 100 first-serve wins − 39 second-serve wins). Total service points 219 + 203 = 422; Federer therefore 218. This is an independent arithmetic reconciliation across different record structures, **not proof of independent collection**: both datasets are maintained by Sackmann, and upstream lineage for these particular aggregate values has not been established. Wimbledon corroborates the final score, ITF corroborates the 14-point margin, but neither supplies an independently coded 422-point sequence here. Existing case audit records a 203/218 discrepancy on Djokovic's own site; do not suppress provenance disagreement.

Fresh raw-file retrieval was attempted: terminal network DNS was unavailable, and the web fetch rejected the 5.17 MB CSV as too large. This audit therefore verifies the retained original-format subset, not an unchanged upstream revision today. The public dictionary, README, charting report, ITF report and official score PDF were retrieved successfully. MCP requires attribution and carries CC BY-NC-SA 4.0; no new access dependency is proposed.

## Reproduction for later acceptance checks

Read the JSON using Python 3 standard library. Assert unique `(match_id, Pt)` and ordinal range; count `PtWinner` independently. Define set index as `1 + int(Set1) + int(Set2)`. For this actual match, define tiebreak membership by `Gm1 == Gm2 == 6` in sets 1–4, `Gm1 == Gm2 == 12` in set 5. Assert the three disjoint groups' ID union equals the complete ID set and pairwise intersections are empty. Assert every row keeps its original winner and identity before/after any visual arrangement. Independently replay tennis scoring and verify all pre-point fields, as above; this catches score-label/serving errors a total-count test cannot. The existing `python3 docs/research/wimbledon_case_probe.py` is a convenient secondary recount but is not the independent replay performed for this audit.

Before implementation, acceptance fixtures should include points 76/81/87, 88/125, 188/198, 359/360, 413/422, the named-player score orientation at service changes, and all subset denominators. No source-code or UI acceptance fixtures have been added during planning.
