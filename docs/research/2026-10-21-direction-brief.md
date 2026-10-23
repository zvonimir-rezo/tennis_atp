# ATP product discovery: decision briefing

**Interview update:** the user selected one finished historical Margins investigation for statistically minded tennis fans, with an authored verdict, inspectable/challengeable evidence and dramatic sports-editorial visuals. The earlier two-case minimum and novice-audience test are superseded. See the [current direction and proposed next experiment](2026-10-21-margins-direction.md); the two options below remain the original comparative investigation.

2026-10-21. **Provisional recommendation: Margins, an interactive anatomy of remarkable tennis matches.** Its opening experience is one verified paradox made tangible by moving the same point records between counting and tennis scoring. This is a recommendation to test, not a settled direction or a demonstrated audience response.

This briefing supersedes the direction-ranking and interview criteria in the earlier discovery note. **Enjoyment of implementation is not a selection criterion.** The intended outcome is a portfolio experience with a strong concept, visual execution and satisfying interaction. Practical utility is a bonus. Only two directions clear the threshold; adding a third would dilute the investigation.

## Evidence and actual capabilities

The application was inspected in source and exercised again in the browser. Existing evidence probes were rerun, rather than treating their earlier conclusions as authority. Full technical evidence: [implementation audit](2026-10-21-project-discovery.md); freshly checked external evidence: [reference audit](2026-10-21-reference-audit.md).

- **Working:** CSV ingestion, pre-tournament player states, Elo, mirrored feature generation, logistic/boosted models, a local matchup form, probabilities and fair-odds arithmetic. The browser produced Alcaraz 41.7% versus Sinner 58.3% on clay. It starts with a form; after submission it shows two progress bars and fair odds. There is no match replay or evidence exploration.
- **Documented or inferred, not established:** dependable live inference, calibrated GUI forecasts, profitable betting, tactical/psychological explanations, and exact match-day fatigue. The GUI serves a different artifact from the chronological training workflow, uses overall Elo where training used blended Elo, and takes the first ranking snapshot rather than the latest. It is not a historical replay of the evaluated model.
- **Reproduced:** rebuilding 25,901 matches creates 51,802 mirrored rows. Four selected saved/rebuilt feature columns agree exactly. This is a selected invariance check, not a comprehensive feature test suite. Existing outputs and source CSVs were preserved.

### One representative match, end to end

`atp_matches_2025.csv`: `2025-520`, match 401, Alcaraz–Sinner, Roland Garros final. The source date is **May 26**, the tournament-start date; the match was played **June 8**. Normalized ID: `2025-520_401_207989_206173`.

The feature builder snapshots every match in a date batch before applying its updates. Consequently the final uses pre-tournament histories: Alcaraz overall/clay Elo 2095.84/2080.35; Sinner 2194.88/1930.71. Both have 90% last-ten win rates and show 19 days since their previous recorded tournament-date match. Same-event rounds are excluded. Those are conservative cutoff features, not final-day physical measurements.

A logistic fit through 2023, calibrated on 2024, assigns Alcaraz **53.10%** for this 2025 feature row; blended Elo says 53.63%, rank/points logistic 41.63%. Applying the GUI's all-years artifact to the row gives 53.77%, but it has seen the evaluation era. Typing the two names into the actual GUI gives 41.7% using latest saved state and wall-clock age/rest instead. The trace exposes a break between evaluation and user experience; it does not validate the GUI forecast.

From the box score, Alcaraz wins 117 service points plus 75 return points = **192**. Sinner wins **193**. The independently downloaded volunteer Match Charting Project sequence contains all **385** unique points and matches those totals; the [official Roland Garros account](https://www.rolandgarros.com/en-us/article/rg2025-rg-live---day-15-sunday-8-june) corroborates the outcome, totals and three saved championship points. This is a stronger verified product specimen than a headline about a small prediction improvement.

### Probability checks

One independent observation per match; both players need at least 20 prior recorded ATP matches. Fit through 2023, calibration 2024, diagnostic evaluation 2025: **2,179 matches**, excluding 765 raw 2025 matches. This is not an untouched future test: the project's notebooks previously inspected 2025.

| Benchmark | Log loss, lower is better | Brier, lower is better |
|---|---:|---:|
| Rank/points logistic | .62588 | .21883 |
| Overall/clay-or-other-surface Elo blend | .62388 | .21809 |
| 19-feature logistic + temporal sigmoid calibration | .61115 | .21257 |

Removing retirements/walkovers/defaults/abandonments leaves 2,067 matches and retains the model's advantage (.60444 versus Elo .61458 and rank .62189 log loss). Calibration bins remain imperfect: 638 favorites forecast at 64.68% win 66.93%; 383 forecast at 74.32% win 71.80%. Sparse tails and prior model selection limit stronger claims. [Official calibration documentation](https://scikit-learn.org/stable/modules/calibration.html) explains why overall scores alone do not establish reliability. Neither these results nor the inspected [comparative research](https://vuir.vu.edu.au/34652/1/jqas-2015-0059.pdf) establish a bookmaker edge.

The worst errors are useful constraints: Goffin's completed Miami win over Alcaraz received 7.60%; Griekspoor's Shanghai win over Sinner received 3.60% but ended in retirement. A low-probability outcome is not automatically a bad forecast; injury/non-play affects targets. A spectacular apparent minority-point win by Bergs over Rublev fails box-score consistency checks and was rejected as a story.

### Material constraints and consequences

| Constraint | Verified boundary | Product consequence |
|---|---|---|
| Coverage | Local 2017–2025 plus partial 2026: 25,901 matches, 1,172 players; team events included | No all-time/career-complete or lower-tour claim |
| Freshness | Latest local tournament date April 22, 2026; ranking snapshots end May 4; original ATP upstream currently returns 404 | A pinned historical edition is feasible; a current service needs a verified refresh path |
| Granularity | Base files contain match/set scores and box counts, no point order or tracking | No invented rallies, 3D trajectories, exact shot locations or tactical causes |
| Missingness | Minutes missing 6.33%; serve totals 4.34%; loser rank 1.33%; about 30% of rolling serve snapshots missing | Show source/sample coverage; avoid automated interpretations of imputation |
| Chronology | Tournament-date precision; batch exclusion avoids current-row leakage but loses same-event history; overlaps can still impair true match-day ordering | Label pre-tournament cutoffs; do not sell fatigue or live-state fidelity |
| Reproducibility | No locked environment; much app code untracked; current upstream commit alone lacks it | Pin source/data/runtime for a finished demo; discovery does not require unrelated cleanup |
| Extra point source | Public MCP index and dictionary readable without key; downloaded index 7,566 men's records, latest May 21, 2026, many blank times; real final subset recovered | Curated cases are available; complete/unbiased/live coverage and video sync are not |
| Terms | Local ATP README and original MCP README specify attribution, noncommercial use, share-alike; no video rights verified | Carry provenance and license with the derived data; commercialization/portfolio-specific rights interpretation remains unresolved, not silently approved |
| Odds | Existing odds join demonstrably mismatches players/events; provider access/provenance and quote times not verified | No ROI, real opportunity or market-beating promise |
| Maintenance | Manual charting, corrections and source availability vary | Freeze a small edition; expansion requires record checks and editorial effort |

## Direction A: Margins

**One sentence / reason to open.** An interactive anatomy of famous matches that lets you pull one apparent tennis contradiction apart until you can explain it yourself.

**First 30 seconds.** A large typographic proposition, “More points. Less of the match,” sits above two fields of 192 and 193 point marks. One action, “See the sets,” carries the very same marks into five scoring groups. Sinner wins the first two; Alcaraz the last three. The fourth set has 39 points each, yet Alcaraz wins it 7–6. A clear next invitation opens the championship-point boundary. No search form or knowledge of model metrics is required.

**Defining interaction and visual identity.** Persistent evidence changes arrangement under the visitor's control: point totals → score structure → one precise boundary. The finished form should include a game-level expansion so the explanation goes beyond simply repeating the result. An alternate ending at a championship point demonstrates a rule: if Sinner wins that point, the match ends. It does not pretend to know how later tennis would have unfolded.

Editorial typography (large, tightly composed serif headlines; quiet sans-serif labels), a paper/ink or dark-ink edition, clay and green player identities reinforced by circle/square marks, hairline structure and generous negative space. Motion should track identity and aggregation, never decorative particle drift. No stadium photograph, stock dashboard cards or gratuitous 3D court is necessary. A complete composition has one question, one dominant field of evidence and one next action.

References explain the mechanism rather than prescribe a skin: [Pudding's Pockets](https://pudding.cool/2018/08/pockets/) lets a visitor test an abstract comparison using concrete objects; retain that inspectability. [Gapminder's official guide](https://www.gapminder.org/tools/assets/guide.pdf) preserves identity and gives control over time; use that continuity at match scale. [You Draw It's creator](https://driven-by-data.net/2015/05/28/college-chart-game/) explains why eliciting an expectation makes the reveal meaningful. These principles support a design hypothesis, not a proven effect in this product.

**Real data specimen.** The RG2025 final has 385 points; set-level Alcaraz/Sinner point totals are 34/41, 39/41, 32/28, 39/39, 48/44. Points 264–266 are the saved championship points. At point 264 Alcaraz serves at 0–40, trailing 3–5 and one set to two. Awarding that point to Sinner would immediately finish the match 6–3 in set four. The study uses these real records, not synthetic trajectories or a modeled win-probability curve.

**Distinctiveness relative to inspected products.** Tennis Abstract already provides point descriptions, shot tables and a Lottery Matches list of minority-point winners. The fact is not novel. Margins would earn its place through a short, authored question, a coherent transformation and a bounded discovery the reader can reproduce. RallyIQ already supplies scouting/style/matchup tools; a generic tactical explorer offers weaker differentiation. No claim of category-first originality is made.

**Continue / return / share.** Within a case, discovering the next boundary should create curiosity. Across cases, a contrasting question supplies another short experience. Sharing a specific surprising explanation is more plausible than sharing a generic profile. All three behaviors remain hypotheses. A finite edition can succeed as a portfolio piece without becoming a weekly publication.

**Smallest complete version.** Two carefully verified, authored cases with one shared visual grammar, one self-contained reveal apiece and a deliberate ending linking to the other case. The first is this final; the second must be found and validated, not invented now. If it needs a different interaction, cut the collection claim and finish one exceptional essay instead. Include source/coverage details, keyboard/touch access and reduced-motion paths. Exclude betting, live feeds, comprehensive profiles, automatic story generation, video hosting/sync, tactical prescriptions and psychological labels.

An additional source check finds Djokovic–Federer, Wimbledon2019 final (`2019-540`, match 226): the local box score gives Djokovic 204 points to Federer's 218, and its [actual charted match page](https://www.tennisabstract.com/charting/20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic.html) is accessible. That confirms another relevant specimen exists. It repeats the same minority-point paradox, however; it does not yet establish a contrasting second investigation or sustainable editorial variety. No second full point sequence was downloaded or validated in this pass.

**Hardest assumption / maintenance / strongest rejection.** The scoring interaction must reveal something richer than “tennis counts games.” A visitor who already knows the result may understand everything from the first sentence; a novice may need too much explanation. Each additional case requires verification and editorial composition. Reject if the study cannot generate a useful self-discovered explanation or a second case of equal quality. These are experience and scope risks, not judgments about whether writing is enjoyable.

**Portfolio proof.** Information and interaction design, typography, purposeful motion, domain/state modeling, reproducible data transformations, responsive execution and restraint about unsupported inference. It would demonstrate a finished experience more directly than an additional model architecture.

**Cheapest observable test.** Current disposable study plus a second manually prepared contrasting case, no backend. Observe five people individually without introducing the controls. In 30 seconds, at least four should identify and operate the central action; in two minutes, at least four should explain the game/set reset mechanism using the displayed evidence rather than repeat the headline. Leave a second case available without prompting: at least three should open it voluntarily. Record the first wrong interpretation and where each person stops. Failure should change/cut the mechanism, not add menus. These thresholds are small falsification screens, not demand estimates.

## Direction B: Read the Match

**One sentence / reason to open.** A compact probability game that makes you stake a degree of belief on a historical matchup and exposes how well your confidence holds up across a session.

**First 30 seconds.** One matchup fills the screen, with a dated surface/ranking/form dossier and a prominent probability line. The visitor places their confidence and locks it. Rank, Elo and model markers then appear; only afterward does the result open. The next ordinary match is already within reach. The hook is “how certain am I?” and the repeated commitment, not a recommendation to place money.

**Defining interaction and visual identity.** Commit → compare → reveal → accumulate. A single horizontal confidence instrument becomes the organizing geometry. Use a spare broadcast-scoreboard aesthetic: large tabular numerals, condensed sporting labels, sharp high-contrast fields and one active accent; avoid coins, casino colors and celebratory animations for merely selecting a winner. Reveal timing and marker motion make differences legible. A session-end calibration view grows out of the same confidence line. It must not pronounce a participant calibrated from ten answers.

The transferable reference is [You Draw It](https://driven-by-data.net/2015/05/28/college-chart-game/): make the visitor's prior judgment visible before introducing evidence. Tennis Abstract forecasts and the current ATP form are direct neighbors; the distinction would be accumulated probabilistic feedback and an honest baseline comparison, not prediction as a feature. The visual direction is proposed; unlike A, it has no rendered interaction study in this investigation.

**Real data specimen.** Goffin–Alcaraz, Miami2025: freeze the pre-tournament dossier, elicit a probability, then reveal Goffin's 5–7 6–4 6–3 win and the model's 7.60% assessment. This is an example card, not a basis for selecting only upsets. The actual fixed deck must include ordinary outcomes and use the same cutoff and eligibility rules as its benchmarks. A model losing one unlikely match does not discredit its probability. Across a session, use Brier score, not winner-pick streaks.

**Distinctiveness / continuing / sharing.** A visitor compares their confidence with three transparent benchmarks and sees where they systematically overcommit. Another session might be attractive because it challenges the visitor rather than delivering another analysis. A shareable session record could prompt comparison, but appeal/return remain unobserved. It is a clearer ML showcase than A, with a weaker assured visual payoff.

**Smallest complete version.** Twenty pinned historical match cards divided into two short sessions, pre-tournament facts, a probability input, benchmark/result reveal and a cumulative proper score with plain interpretation. No login, live predictions, money, marketplace, social leaderboard, parameter-tuning laboratory or general tennis search. Mark remembered outcomes and exclude them from the visitor's honest assessment.

**Hardest assumption / maintenance / strongest rejection.** Fans may remember results; disguising players removes attachment and makes the task arbitrary. Even unknown historical outcomes may feel like guessing, while aggregate feedback arrives slowly. Deck selection must not manufacture drama or make the model appear strong; versioned facts/models need periodic verification, not daily operations. Reject if novices cannot make a reasoned estimate and experts recognize most results, or if the emotional reward is only a lucky upset. A more elaborate game cannot fix those core failures.

**Portfolio proof.** Temporally evaluated ML, probabilistic reasoning, game/feedback design, experimental judgment and a tightly paced interface. It supports no claim to beat markets or teach better forecasting without larger evidence.

**Cheapest observable test.** Ten paper or simple form cards and a second unprompted session. Five tennis followers mark known results. Provisional support: at least four can enter a probability and explain the feedback without coaching, at least three voluntarily start session two, and at least four understand why a 70% favorite losing once need not be a poor forecast. If over 20% of cards have known outcomes, revise the deck premise before engineering. This tests appeal/comprehension, not improved calibration.

## Why no third direction

A spoiler-free replay curator has concrete firsthand workarounds behind it: [viewers hide duration and thumbnails](https://www.reddit.com/r/tennis/comments/1n40i9h/why_do_they_spoil_highlights_itd_be_so_much/). However TennisTV already has spoiler controls; availability, subscriptions and player handoff dominate the experience. Its self-contained visual/interaction payoff is weaker for this brief. A generic rivalry/style atlas similarly overlaps Tennis Abstract, UTS and RallyIQ without a verified exceptional central insight. They were considered and screened out, not developed into additional product proposals.

## What outside evidence does and does not establish

[A match-analysis discussion](https://www.reddit.com/r/tennis/comments/10kcvzy/) records people seeking patterns/reasons, recommending charting/video sources and writing navigation guides. [A player-profile request](https://www.reddit.com/r/tennis/comments/vg5s7o/) shows a reader using Wikipedia prose and missing equivalent coverage for Báez. **Observed:** concrete explanatory/navigation workarounds in self-selected historical discussions. **Interpretation:** a guided question is worth testing. **Speculation:** these people would prefer Margins, return, or share it. No participant observation, novelty proof, market-size estimate or demand validation occurred.

The study was operated by the investigator: points/sets switch, fourth-set game expansion, recorded championship sequence and alternate immediate ending. Browser operation confirms functionality, not uncoached comprehension. Visual quality should be assessed against observable composition criteria: the question dominates before metadata; labels remain legible at narrow widths; player encoding stays consistent; mark identity persists through motion; every action has a visible result; reduced motion still explains the relationship. A visual reviewer should be able to point to a specific hierarchy or continuity failure, rather than say “make it modern.”

## Decision tree and pending interview

The first branch concerns the desired visitor experience, not implementation enjoyment: **discover a surprising mechanism (A) or commit and test personal judgment (B)?** Recommend A provisionally. Then resolve audience tennis knowledge and desired emotional response, expressive visual treatment, finite edition versus ongoing service, exact exclusions, and the next falsifiable experiment. Ask one consequential question per turn and adapt; do not assume the whole tree is settled.

The direction is **not chosen yet**. No production product was built or published. The current study tests only A's first specimen; a second case, human tests and final visual polish remain unverified. Independent review checked all 385 winners, 59 game records and the alternate ending; it prompted the addition of a games view and removal of an inadequately evidenced competitor claim.

## Reproduction checkpoint

Base commit remains `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`. Preserve pre-existing deletions and untracked implementation. Existing GUI ran locally with `/private/tmp/atp-discovery-313/bin/python`; feature/model probe completed successfully again with `PYTHONPATH=src:.`. Evidence outputs are under ignored `reports/discovery/`. The sensitivity probe was rerun separately. No upstream CSV, model, production module or dependency declaration changed.

Next action: brief the user, display the study, ask the experience-choice question, and record their answer before narrowing visual identity or scope.
