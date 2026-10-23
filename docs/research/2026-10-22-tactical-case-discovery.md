# Two ways forward: Djokovic–Medvedev, US Open 2023

Investigated 2026-10-22. Research candidate for Margins; no reusable system or application change. Match: 10 September 2023 final, Djokovic over Medvedev, 6–3 7–6(5) 6–3. MCP identity `20230910-M-US_Open-F-Novak_Djokovic-Daniil_Medvedev`, charted by Zindaras. [Original MCP match report](https://www.tennisabstract.com/charting/20230910-M-US_Open-F-Novak_Djokovic-Daniil_Medvedev.html).

## The discovery

In the second set, Djokovic won **all eleven serve-and-volley points**, but only **three of eleven points containing one of his own drop shots**. The better like-for-like cut keeps Djokovic serving: **11/11 serve-and-volley, 1/5 drop-shot points, and 25/36 other service points**. These are complete, disjoint service-point groups, including tiebreak serves. A serve-and-volley point is explicitly coded as a successful first/second serve followed by an approach (`+`); a drop-shot point contains Djokovic's `u` (forehand drop) or `y` (backhand drop). All selected drops occur once per point, so no shot is being counted as an additional point.

This sharpens the familiar story that Djokovic escaped a grinding second set by changing the geometry. His serve-and-volley plays and points containing his own drop shots had very different recorded outcomes. This comparison identifies shot patterns, not intent or proof of where Medvedev stood. In particular, the one successful service drop-shot point, ID84, is a **counter-drop** after Medvedev's own drop shot; it cannot be described as a preplanned attempt to pull Medvedev forward. Even controlling for the server does not match the incoming balls or opportunities.

The tension is visible inside one service game, rather than only in aggregate statistics. At **5–6**, Djokovic lost both points containing his own drop shot (IDs **143 and 154**) and won all four explicitly coded serve-and-volley points (IDs **147, 150, 153 and 155**). ID **150** saves Medvedev's set point at 40–AD. ID **154** is a missed drop shot on Djokovic's game point; ID **155** immediately restores game point with a serve-and-volley play. Earlier, ID **122** uses serve-and-volley to save break point at 3–4. The whole game remains visible, including two double faults and other rally outcomes; these tactical groups do not account for every point.

This is a descriptive contrast within one match/set. Five service drop-shot points are a tiny, selected sample; service context, serve quality, rally length and the ball available to attack still differ. The evidence cannot establish how many points Djokovic would have won had he chosen the other tactic.

All counts above derive from original [MCP raw point records](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-points-2020s.csv), replayed and classified by [tactical_case_probe.py](tactical_case_probe.py). The bounded second-set 11/11 serve-and-volley count is also stated in the [ATP match report](https://www.atptour.com/en/news/djokovic-medvedev-us-open-2023-final): the fresh indexed excerpt was readable, although direct full-page retrieval returned 403. The [US Open's own report](https://www.usopen.org/amp/en_US/news/articles/2023-09-10/novak_djokovic_wins_24th_grand_slam_singles_title_at_2023_us_open.html) confirms the score, set point saved and overall tactical context. The unusual drop-shot comparison is an analysis of the raw chart, not a claim quoted from those reports.

## Exact evidence

The second set is IDs **59–168**, 110 points: Djokovic 58, Medvedev 52. Djokovic serves 52 points and wins 37. Server/returner labels include tiebreak service points. The comparison does not silently count Medvedev-service drop shots as Djokovic-service points.

| Djokovic service points, second set | Won / points | Exact IDs |
| --- | ---: | --- |
| Explicit serve-and-volley | 11/11 | 74, 86, 111, 122, 132, 147, 150, 153, 155, 163, 167 |
| Contains his own drop shot | 1/5 | 84, 116, 121, 143, 154 |
| Other service points | 25/36 | Complete membership in the evidence JSON |
| Total | 37/52 | Complete second-set service population |

There is **zero overlap** between own-drop and serve-and-volley points in this set or the full match. The single successful service drop-shot point is the counter-drop at ID84. Six additional own-drop points occur on Medvedev's serve: **97, 107, 127, 139, 140 and 165**; Djokovic wins only IDs97 and140. Thus the full-set drop group is 3/11, with no repeated shots inflating the denominator.

Whole-match context: Djokovic's 14 drop shots occupy 14 distinct points and yield four point wins; those counts agree exactly with the frozen [ShotTypes table](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-stats-ShotTypes.csv), including one forehand and thirteen backhand drop shots. These are points won after a drop, not fourteen point-ending drop attempts or a direct-error rate. Fourteen drops include one direct winner, one forced ending and three unforced endings; many points continue after the drop.

## What a reader would discover

Opening question: **“Two ways out of the baseline battle. Did both work?”**

1. Keep the second-set record and score together. Surface the familiar serve-and-volley escape, then disclose the opposite drop-shot outcomes.
2. Let the reader compare all own-drop points with the **serve-only** cut. This makes the initial denominator objection answerable and leaves the tiny sample visible.
3. Step through the 5–6 service game. Show its full sequence, then highlight the four serve-and-volley wins and two drop-shot losses. The set-point save is a concrete moment where the tactic and score meet.
4. End with the selection caveat: the same player serving does not make shot choices interchangeable experiments.

Bounded verdict: **Djokovic's second-set serve-and-volley escape was real. His drop shots had a very different result, even when he was serving.** This is enough for an authored investigation without claiming a universal tactical rule or assigning psychological causes.

The court can identify a schematic approach versus a drop-shot exchange, but it must not invent physical coordinates or animate recorded trajectories that these codes do not contain. The exact point inspector should retain the source code and pre-point score behind every example. These are proposed evidence views, not instructions to implement a reusable renderer now.

## Verification, reproduction and source disagreement

Run from the repository root:

```sh
python3 docs/research/tactical_case_probe.py
```

Standard-library probe; reads retained downloads and writes only ignored `reports/discovery/case-search-tactical/`. The script independently generates all **215/215** pre-point scores, set/game states, servers and game indices from winners, recovers 6–3 7–6 6–3, and checks every state against the raw record. Per-set and total service counts/wins agree with all eight stored MCP Overview rows. Local ATP2023 player/event/final identity, both service-point totals (109/106) and Djokovic service points won (75) agree. All14drop shots and their4point wins agree with ShotTypes. All focal classifications, zero overlaps and the set-point/break-point examples are asserted. Full input and subset SHA-256 values and exact record memberships live in `tactical-evidence.json`. A separate parent-agent character scanner independently reproduced all selected memberships, outcomes, zero overlaps and the5–6game, saved as `independent-parent-audit.json`.

Frozen 215-point JSON SHA-256: `7710e3720626312e53bac2ce5cd87461f06a9fb14f1ba5abf40c936db804c73a`. Raw full2020s file SHA-256: `2cd43f73e0530a47ea4c02b99dae40177ca6d58a8ccf9189358eb05dffb4be9a`.

Notation checked against the source author's [quick start guide](https://www.tennisabstract.com/blog/2015/09/23/the-match-charting-project-quick-start-guide/) and the Instructions shared strings in the public [MatchChart0.3.2 spreadsheet](https://github.com/JeffSackmann/tennis_MatchChartingProject/blob/master/MatchChart%200.3.2.xlsm). Its definitions explicitly identify `u/y` as forehand/backhand drop shots and `+` as an approach, including serves. Leading `c` lets must be removed before alternating shots: mishandling them misassigns IDs121 and154 and misses serve-and-volley ID132. Selected raw code and independent aggregate agreement catch that error. The downloaded spreadsheet and extracted instruction strings are retained in the ignored research output. [MCP dictionary](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/data_dictionary.txt) defines scores/server/winner fields.

**Disagreement preserved:** the entire-match raw chart and MCP SnV aggregate identify **19/21** serve-and-volley outcomes; the official US Open report gives **20/22**, and overall net points also differ (MCP37/43, official37/44). One successful serve-and-volley/net event appears differently classified between sources. Its identity and reason are unresolved; no source point is relabeled to force agreement. The selected second-set **11/11** agrees with the ATP report's indexed description and is reproducible from the explicit codes. The case must stay explicitly scoped to set two; do not present the MCP whole-match total as the official count. Overview and raw chart are related source products, not independent witnesses.

Attribution: Jeff Sackmann / Tennis Abstract Match Charting Project, charted by Zindaras, [CC BY-NC-SA4.0](https://github.com/JeffSackmann/tennis_MatchChartingProject#license). No video, betting model, physical tracking data or new service is required.

## Why this candidate

Exploratory raw scans covered Alcaraz–Medvedev Indian Wells2023/2024 finals, Wimbledon2023/2024 semifinals, USOpen2023 semifinal and Beijing2024 semifinal, Alcaraz–Zverev RG2024 final, Alcaraz–Sinner RG2025 final and Djokovic–Alcaraz Wimbledon2023 final. This was editorial search, not a complete population scan or proof of novelty.

- **RG2025 final:** after correct let handling, Alcaraz drop points improve from5/13 in sets1–4 to7/9 in setfive. A viable future pattern, but the raw total22 alone is familiar, and the late/early split risks a small-sample turning-point story. It also reuses a match already investigated by this project.
- **RG2024 final:** Alcaraz wins all7drop points in the third set he loses, then only1/4 in the fifth set he wins. Interesting, but raw/aggregate classification auditing was not completed here; it remains a candidate, not an established publishable case.
- **Indian Wells2023 final:** Alcaraz wins7/11 own-drop points and9/10 explicit serve-and-volley points against Medvedev. Those preliminary raw patterns match the expected story more than they complicate it; not selected.
- **USOpen2023 final whole-match20/22 headline:** too familiar by itself, and inconsistent across official/MCP source classifications. The useful discovery is the second-set contrast and the exact5–6game.

Unknown: whether expert fans find this framing surprising and whether the proposed manipulation clarifies it. Numerical verification establishes the recorded pattern, not audience appeal or tactical causality.
