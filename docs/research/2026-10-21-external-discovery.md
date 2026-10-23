# ATP discovery: external evidence and disposable probes

Investigated 2026-10-21. This note records external evidence; the companion project investigation owns the implementation and model audit. No production implementation or paid service was added.

## Findings that constrain the choice

- **Observed:** the original [ATP repository](https://github.com/JeffSackmann/tennis_atp) and [2026 raw file](https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2026.csv) returned HTTP 404 through both web retrieval and a direct Python HTTP request. The cause and permanence are unknown. Mirrors exist, but a mirror is not evidence of a continuing update service. A historical, pinned experience is currently easier to promise than a current-tour service.
- **Observed:** the local original README specifies CC BY-NC-SA 4.0, attribution and non-commercial use. It also explains that `tourney_date` usually means tournament-start Monday, not match start, and statistics may be absent or removed after sanity checks. The [MCP original README](https://github.com/JeffSackmann/tennis_MatchChartingProject) independently states the same license family, manual shot charting, and periodic GitHub updates. Its dated “5,000 matches” prose is not a current count.
- **Observed:** MCP raw files remain publicly downloadable without a key. The downloaded men's match index has **7,566 rows**, latest valid date **2026-05-21**. The [live chart index](https://www.tennisabstract.com/charting/) contains October 2026 matches. Thus site freshness and downloadable GitHub freshness differ. This is not a live-data dependency.
- **Observed:** the raw MCP index contains 3,472 empty `Time` fields and one malformed date, `RR`, for `20240915-M-Davis_Cup_World_Group-RR-Botic_Van_De_Zandschulp-Matteo_Berrettini`. Times such as `4pm`, `14:30`, and `8:45 PM` are human text without timezone guarantees. The [point dictionary](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/data_dictionary.txt) provides score, server, winner, and shot codes; it does not supply tracking coordinates or video synchronization.

**Interpretation:** editorial case selection can absorb these limits; universal tactical forecasts, match-accurate fatigue estimates, live recommendations and automatic video alignment cannot simply be assumed available.

## Verified new-data experiment

Public files were downloaded to `/private/tmp/atp-discovery-external/`; upstream and project CSVs were not edited.

| File from MCP `master` | Bytes | Parsed records | SHA-256 |
|---|---:|---:|---|
| `charting-m-matches.csv` | 1,141,817 | 7,566 | `d8dce1ad8d12c04efa01da587441b54ece8e8100530660528312244f632efe80` |
| `charting-m-stats-Overview.csv` | 6,651,805 | 56,850 | `9b08d763e1209dec276206998b96823731f0351ab9b86d25415a7e3dd313290c` |
| `charting-m-stats-ShotTypes.csv` | 33,357,442 | 352,384 | `683dfe27907e61388bda8400b33fa42a23ed030b3399775bc1b787ab69e1d47b` |

Source base: [MCP raw repository](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-matches.csv).

A disposable linkage normalized unordered player names (Unicode decomposition, lowercase, alphanumeric), required the same round, and allowed a chart date from three days before through 21 days after ATP tournament date. It uniquely linked **552 of 2,944 local 2025 ATP rows, 18.8%**, with no ambiguous 2025 links. For 2017–2024 the corresponding rates were 7.5%, 8.5%, 18.4%, 10.1%, 12.0%, 20.4%, 20.0%, 21.4%; some years had 3–4 ambiguous links. This is a feasibility probe, not a production join or a definitive coverage estimate: naming variants and round conventions can lose real matches; date-window matching can accept wrong events. Hand-verify a curated set. Federer, Djokovic and Nadal dominate raw chart counts (723, 553, 425), consistent with selection bias rather than representative sampling.

### A fully recoverable real case: 2025 Roland Garros final

`20250608-M-Roland_Garros-F-Jannik_Sinner-Carlos_Alcaraz` exists in metadata, Overview, ShotTypes and the raw 2020s points file. Its metadata gives June 8, 4pm, Court Chatrier, clay, best-of-five, charted by Edo. [Original detailed match report](https://www.tennisabstract.com/charting/20250608-M-Roland_Garros-F-Jannik_Sinner-Carlos_Alcaraz.html).

The raw-point probe streamed [charting-m-points-2020s.csv](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-points-2020s.csv) until that contiguous match block ended. It found **385 unique point numbers, 1–385**. Crucially, their stored order began at point 116 and wrapped to point 1: replay requires numeric sorting by `Pt`, not file order. Sorting recovered three saved championship points, 264–266: Sinner leads two sets to one and 5–3; Alcaraz serves at 0–40, 15–40, 30–40 and wins each point. Point winners total **Sinner 193, Alcaraz 192**, while Alcaraz wins the match. The [official Roland Garros live blog](https://www.rolandgarros.com/en-us/article/rg2025-rg-live---day-15-sunday-8-june) corroborates those point totals; the [ATP's championship-point account](https://www.atptour.com/en/news/alcaraz-roland-garros-2025-final-championship-points) corroborates that score situation.

The shot table contains Alcaraz's **22 drop shots**, versus Sinner's **3**. Alcaraz's rows record four drop-shot winners, three induced forced errors and six unforced errors; points containing those shots split 12 won/10 lost. These descriptive counts can support a reveal or comparison. They do **not** establish that hitting more drop shots would have improved either player's result: opportunity, incoming ball, opponent and selection confound that claim.

Reproduce the point probe with Python's standard library (the network must be enabled):

```python
import csv, io, urllib.request
url = ('https://raw.githubusercontent.com/JeffSackmann/'
       'tennis_MatchChartingProject/master/charting-m-points-2020s.csv')
key = '20250608-M-Roland_Garros-F-Jannik_Sinner-Carlos_Alcaraz'
points = []
with urllib.request.urlopen(url, timeout=30) as response:
    for row in csv.DictReader(io.TextIOWrapper(response, encoding='utf-8-sig')):
        if row['match_id'] == key:
            points.append(row)
        elif points:
            break
points.sort(key=lambda row: int(row['Pt']))
assert len(points) == len({row['Pt'] for row in points}) == 385
assert sum(row['PtWinner'] == '2' for row in points) == 192
print(points[263:266])
```

**Established:** a curated point-and-shot evidence narrative is technically possible at zero new service cost. **Unknown:** appeal, full-file integrity, sustainable freshness, representativeness, visual comprehension, and whether more obscure matches produce equally interesting cases.

### A false-looking discovery worth excluding

Scanning local box scores for the most extreme winner who lost the point count surfaces 2025 Miami R64, Zizou Bergs over Andrey Rublev, 7–5 6–4, with an apparent 63/142 points (44.37%). However, the same row says Bergs faced eight break points and saved five (three breaks conceded), while Rublev faced two and saved one (one break conceded). That cannot produce a completed straight-set win. This row should be treated as a suspect record, not a remarkable tennis fact. No upstream correction was attempted. A case-file direction needs explicit cross-checks; an anomaly generator alone would magnify bad data.

## Adjacent experiences actually inspected

These are observations of publicly rendered pages and links. They are not usage studies. Dynamic tables/authenticated playback were not all available in this environment.

| Product/page | Observed interaction | Consequence for differentiation |
|---|---|---|
| [Tennis Abstract home](https://www.tennisabstract.com/) and [RG final report](https://www.tennisabstract.com/charting/20250608-M-Roland_Garros-F-Jannik_Sinner-Carlos_Alcaraz.html) | Player-first search, match/result tables, forecasts, chart links; report offers serve, return, net and shot breakdowns with comparison context. | “More tennis stats” or an Alcaraz/Sinner comparison is already provided. A staged question → inspect evidence → reveal interaction would need to earn its place. |
| [Tennis Abstract Lottery Matches](https://tennisabstract.com/reports/atp_lottery_matches.html) | Lists matches won despite adverse point/return-point numbers, with TPW and dominance ratio. | The minority-point-win fact itself is not original. Explaining *how the score makes that possible*, with verifiable point sequences, could be a different experience. |
| [Ultimate Tennis Statistics](https://www.ultimatetennisstatistics.com/), [Greatest Matches](https://www.ultimatetennisstatistics.com/greatestMatches), [Head-to-Head](https://www.ultimatetennisstatistics.com/headToHead) | Extensive menus for timelines, rivalries, records and comparison. Dynamic detail was unavailable to the text renderer. | Another comprehensive record portal is unlikely to stand out on breadth. |
| [RallyIQ](https://bigballi.com/RallyIQ/), [Method](https://bigballi.com/RallyIQ/method), [Evolution](https://bigballi.com/RallyIQ/evolution) | Two player inputs → matchup plan; player scout; shot-value decompositions; style fingerprints/similarity; era tactical charts. Method states selection bias and missing tracking context. | A generic tactical matchup or style explorer is already directly adjacent. Its predictive/causal-looking claims were inspected as claims, not independently reproduced. A smaller evidence-first interaction could be different; novelty remains unproven. |
| [Tennis TV replay: Dimitrov–Monfils, Indian Wells 2025](https://www.tennistv.com/videos/4231421/indian-wells-2025-r3-dimitrov-monfils) and [official service information](https://www.tennistv.com/hear-from-us) | The actual replay page is available, with premium playback; the service advertises hide-score/hide-timeline spoiler mode. It excludes Slams, WTA, Challenger, Laver and Davis Cup. | Spoiler hiding is an existing interaction. Cross-match curation could add value, but cannot promise universal video availability or reproduce protected videos. |
| [No Spoiler Tennis launch/user discussion](https://www.reddit.com/r/tennis/comments/13y9s5q/) | Creator documents schedule, player favorites, score reveal and discussion/video search links. Users report lag, timezone problems and thumbnail spoilers. | Another spoiler-aware match list has been built. The site itself could not be accessed after one recovery attempt, so its current UI/availability is unverified. A historical curator avoids its live API maintenance, but broken replay links remain. |

## Firsthand behavior, with limits

- [March 2025 request for spoiler-free recommendations](https://www.reddit.com/r/tennis/comments/1jaelu3/): a viewer with limited time asks what to replay, specifically to avoid choosing a dull match. Several nominate Dimitrov–Monfils at Indian Wells. This exact match exists locally (`2025-0404`, match 340, 181 minutes, 7–6(4) 4–6 7–6(2)), in MCP (March 10, 8:45 PM), and on Tennis TV. This is a verified end-to-end candidate for a curated watch-selection test. It does not show that a statistical score can identify match quality.
- [Spoiler-thumbnail discussion, August 2025](https://www.reddit.com/r/tennis/comments/1n40i9h/): one viewer gets their partner to start a replay so they do not see its duration; others complain that thumbnails and progress bars disclose outcomes. These are concrete workarounds, not evidence of market size.
- [Player-style profile request](https://www.reddit.com/r/tennis/comments/vg5s7o/): the poster wants intelligible strengths/weaknesses rather than raw stats, uses Wikipedia after a suggestion, then cannot find a comparable description for Sebastian Baez. That supports testing explanatory language; it does not justify generating unsupported stroke-level claims from ATP box scores.
- [Stats-source discussion](https://www.reddit.com/r/tennis/comments/cztdfy/): a user tries specific historical queries and ends up asking people because navigation does not expose the desired cut. An author responds with a direct record URL. This supports testing guided question entry and provenance; the requested “youngest ever” claim exceeds this project's 2017-onward scope.

These discussions are self-selected, mostly historical anecdotes. None establishes demand for this project, willingness to return, or the builder's enjoyment.

## Research relevant to predictive directions

[Kovalchik 2016, published paper in the author's institutional repository](https://vuir.vu.edu.au/34652/1/jqas-2015-0059.pdf) compares 11 approaches against bookmakers on 2,395 ATP matches from 2014. Rank-based and Elo approaches are strong; performance varies materially across player rank levels. This is a reason to demand honest simple baselines and subgroup checks, not proof of a modern betting edge. The paper's own probability/calibration discussion is more relevant than a headline accuracy percentage.

[Vaughan Williams, Liu and Gerrard 2019](https://www.ntu.ac.uk/__data/assets/pdf_file/0024/830562/how-well-do-elo-based-ratings-predict-professional-tennis-matches.pdf) compares rank, overall/surface Elo and odds at Wimbledon 2018. Bookmaker odds perform best for men's accuracy and calibration in that event. Its single-tournament sample and optimized mixture weights limit extrapolation. Neither paper validates this repository's implementation or current model.

[Kovalchik and Reid's dynamic calibration paper](https://www.sciencedirect.com/science/article/pii/S0169207017301395) proposes combining pre-match information with empirical-Bayes updates for within-match forecasts. Only its accessible abstract/description was reviewed. Point records make a score-state demonstration feasible, but they do not supply a validated live probability model automatically.

Historical odds are **not a verified new dependency**: Tennis-Data's [data page](https://www.tennis-data.co.uk/alldata.php), notes and a proposed 2025 CSV returned 403 through the web and direct HTTP recovery. No account, subscription or proxy was used. Their [disclaimer](https://www.tennis-data.co.uk/disclaimer.php) does not establish redistribution rights. A betting-ROI or bookmaker-comparison promise must wait for a readable, licensed sample with a documented quote timestamp.

## Three interactions worth considering, all provisional

1. **Match case files:** begin with a real paradox or claim, ask the visitor to form a view, then let them reveal point/shot evidence and its limits. RG2025's 192–193 points and three saved championship points provide a verified case. The return reason would be another short, authored case, not a bigger dashboard. Cheapest behavioral test: two manually curated cases; observe whether 3/5 tennis viewers voluntarily open the second and can explain the first correctly. Biggest rejection reason: editorial writing/curation may feel like homework for the builder; counts alone are already on Tennis Abstract.
2. **Forecast judgment game:** freeze a historical pre-tournament moment, collect the visitor's probability, show a simple benchmark, reveal the result and score the accumulated judgment. Distinction would be the personal learning loop, not superior predictions. Requires the parent's temporal/calibration audit; famous results can contaminate the game. Cheapest test: ten anonymized/obscure match cards, followed by an unprompted chance to do another set; count voluntary continuation and probability revision. Biggest rejection reason: disguising names removes tennis attachment; revealing names lets memory substitute for judgment.
3. **Spoiler-free replay curator:** one tightly curated evening's choice, based on mood and available time, without giving away the score or exact duration. Dimitrov–Monfils is verified across local record, chart and replay. Existing spoiler mode and No Spoiler Tennis make generic spoiler hiding unoriginal. Cheapest test: give five replay-watchers three concealed cards versus their normal selection method; observe actual replay starts, satisfaction afterwards and one repeat session. Biggest rejection reason: accurate video availability and thoughtful curation may cost more maintenance than the central interaction is worth; statistical closeness is not entertainment quality.

These are proposed experiments, not demonstrated fun, demand or novelty. A portfolio demonstration is strongest when one complete interaction makes the evidence and uncertainty inspectable. Freeze a small historical corpus first; do not expand tours, buy data, automate live scraping or build a broad roadmap during discovery.
