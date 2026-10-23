# External reference audit, 2026-10-21

A second inspection of the discovery evidence. Observed = retrieved source, rendered interface, or recomputed record. Interpretation = design consequence. Speculation = proposed response requiring human testing. Existing notes are prior evidence, not authority. Building enjoyment is not a decision criterion.

## Data dependencies: verified boundaries

**Observed:** [original ATP repository](https://github.com/JeffSackmann/tennis_atp) again returned 404 in the web tool. This establishes current retrieval failure, not deletion, motive, or permanent unavailability. The project's existing CSVs remain usable as a pinned corpus; ongoing upstream refresh cannot currently be promised.

**Observed:** the [MCP original repository](https://github.com/JeffSackmann/tennis_MatchChartingProject) is publicly readable. Its README describes volunteer shot coding, raw point records, derived aggregates and periodic uploads. It explicitly names CC BY-NC-SA 4.0, attribution and noncommercial use. Public access is not a live-service guarantee. A monetized direction needs a separately settled rights basis; this report does not resolve how the license applies to a portfolio presentation.

The [actual men's match index](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-matches.csv) returned readable CSV through the web tool, including its header and May 2026 records. Recomputed from the earlier downloaded copy: 7,566 records, latest numeric date 20260521, 3,472 blank times; SHA-256 `d8dce1ad8d12c04efa01da587441b54ece8e8100530660528312244f632efe80`. A fresh direct Python request failed because this child environment cannot resolve network hosts; this is not a second independent fresh-file hash. Public web access itself was verified. The [point dictionary](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/data_dictionary.txt) is readable and defines score state, server, point winner and shot notation. It provides neither continuous court coordinates nor video synchronization. Time strings lack timezone guarantees.

**Interpretation:** a hand-checked historical set is feasible. Universal coverage, live alerts, exact fatigue/rest measures, physically accurate ball animation, and synchronized video are separate unverified dependencies.

### Recomputed concrete case

The local downloaded MCP subset for `20250608-M-Roland_Garros-F-Jannik_Sinner-Carlos_Alcaraz` contains 385 distinct point records. Sort by integer `Pt`; stored order starts at point 116. `PtWinner` totals are Sinner 193, Alcaraz 192. Points 264–266 show Alcaraz serving at 3–5 in set four, trailing 0–40, 15–40 and 30–40, winning all three. The [official Roland Garros final-day record](https://www.rolandgarros.com/en-us/article/rg2025-rg-live---day-15-sunday-8-june) corroborates the totals, the three championship points and Alcaraz's victory. The [Tennis Abstract match report](https://www.tennisabstract.com/charting/20250608-M-Roland_Garros-F-Jannik_Sinner-Carlos_Alcaraz.html) supplies the detailed source experience.

**Interpretation:** this is an unusually good first specimen for a scoring explanation. It is not proof of clutch skill or a causal account of the outcome. Reassigning a historical point and replaying subsequent recorded outcomes would be an explicitly artificial rule demonstration: later player decisions would not necessarily remain the same.

## Actual adjacent experiences

| Inspected source and access | Observed experience | Implication |
|---|---|---|
| Tennis Abstract RG25 report, loaded in browser and accessibility snapshot | Dense match header, immediate result, tab-like links for overview/serve/return/key points/rally length/point description/shot tables. Overview includes per-set comparisons. Page explains contextual tour/player hover values. | Another breakdown dashboard repeats existing capability. Differentiation must come from a central question and a legible reveal, not more fields. |
| [Tennis Abstract Lottery Matches](https://www.tennisabstract.com/reports/atp_lottery_matches.html), retrieved actual page | Already lists close/minority-point wins with percentages and dominance ratio. | The paradox is not new. A tactile explanation of how score hierarchy turns points into victory can still differ from its list. Novelty remains unproven. |
| [Ultimate Tennis Statistics Greatest Matches](https://www.ultimatetennisstatistics.com/greatestMatches), actual HTML | Broad navigation for rivalries, timelines, records, rankings and greatest matches. Dynamic data table was not verified in this pass. | A comprehensive tennis archive has established neighbors; claiming better search or completeness would need a direct task comparison. |
| [RallyIQ](https://bigballi.com/RallyIQ/) and [method](https://bigballi.com/RallyIQ/method), actual pages | Two-player matchup input, scouting reports, tactical patterns, style similarity and era evolution. Method explicitly discusses chart selection bias, missing ball/court context and retirement-winner errors. | A tactical/style atlas is already close competition. Its numerical claims were inspected as author claims, not reproduced. No causal endorsement is implied. |
| [Tennis TV service page](https://www.tennistv.com/hear-from-us), actual page | Replays, highlights and an advertised spoiler mode that hides scores/timelines. Official coverage excludes Slams, WTA, Challengers, Laver and Davis Cup. | Spoiler hiding alone has little distinction. External replay links need rights, region and availability checks; a stats app cannot promise protected playback. |

## Outside tennis: principles worth transferring

### Pudding, Pockets

[The actual essay](https://pudding.cool/2018/08/pockets/) loaded in Chrome. Its rendered structure includes 80 measured pocket shapes, an overview-to-average progression, everyday-object selection (phone, wallet, hand), and filters. Selecting an object is presented as a concrete fit test. This pass inspected controls and layout; it did not complete a before/after object-selection measurement.

Parent follow-up operated the actual interaction in the in-app browser: selecting iPhone X displayed 40% women's / 100% men's pocket fit; selecting Pen changed the displayed result to 98% / 100%. A screenshot showed the phone placed within pocket outlines and non-fitting items faded. This confirms the concrete object-to-comparison loop was exercised, beyond the initial control inspection.

**Interpretation:** the compelling mechanism is a directly inspectable physical question, with marks preserving their meaning through aggregation. For tennis, one point token should remain the same token as it moves from a total into its game and set. The visual transformation earns attention by explaining a mechanism. Borrowing pink colors or scroll animation without that mechanism would miss the point. A no-motion final-state path is another useful principle.

### NYT, You Draw It

[Creator Gregor Aisch's own account](https://driven-by-data.net/2015/05/28/college-chart-game/) explains drawing an expectation before revealing the relationship and then showing other reader guesses. Creator evidence, not a current end-to-end inspection of the original NYT interaction.

**Interpretation:** committing a view makes the reveal personally meaningful. For a match case, ask which player won before regrouping the same evidence; for a forecast game, elicit probability before showing model/outcome. Do not confuse a user's single wrong guess with miscalibration: calibration is a repeated-prediction property.

### Gapminder Tools

[Actual tools page](https://www.gapminder.org/tools/) loaded successfully in the browser; this pass did not drive its animation. Retrieved controls and the [official guide](https://www.gapminder.org/tools/assets/guide.pdf) document timeline dragging/play, entity selection, trails, opacity for unselected entities and source information. The current page also presents data doubts.

**Interpretation:** user-controlled time and persistent identity make change inspectable. A tennis career/surface study could isolate one player and preserve its trail. This is weaker than the match specimen unless a specific reversal or comparison is first demonstrated; an animated field of dots alone supplies visual noise. The uncertainty disclosure is part of its coherence, not an appendix.

Radio Garden and Evolution of Trust were fetched but not sufficiently exercised; they are not counted as inspected interaction evidence in the recommendation.

## Firsthand behavior: narrow evidence, no demand claim

- [2022 player-profile request](https://www.reddit.com/r/tennis/comments/vg5s7o/): a person requests intelligible strengths/weaknesses; after a Wikipedia suggestion they inspect several players and find the format useful but cannot find equivalent coverage for Báez. **Observed workaround:** use prose biographies. **Interpretation:** a human-readable question can be more approachable than raw columns. **Not established:** willingness to use this particular product or that box scores describe every requested stroke.
- [2023 request for match analysis](https://www.reddit.com/r/tennis/comments/10kcvzy/): users seek shot patterns and reasons for wins/losses, recommend MCP and analysis videos, and describe difficulty navigating Tennis Abstract. One user supplies a personal guide to filtering/searching source pages. **Interpretation:** explainability and finding the right cut are testable needs; a broad replacement portal is not thereby justified.
- [2025 spoiler discussion](https://www.reddit.com/r/tennis/comments/1n40i9h/why_do_they_spoil_highlights_itd_be_so_much/): one viewer has their partner start replay playback to avoid seeing total duration; others describe progress bars and winner thumbnails spoiling outcomes. **Interpretation:** hiding the score is insufficient for a spoiler-free curator. **Not established:** size of this audience, freshness requirements or reliable cross-provider integration.
- [No Spoiler Tennis creator/user thread](https://www.reddit.com/r/tennis/comments/13y9s5q): creator describes grouping fragmented tournament information; a viewer says replay allows skipping between-point time. **Interpretation:** the established workaround and existing app narrow differentiation to actual selection quality or a more coherent reveal.

These are self-selected historical discussions, retrieved through search indexing when direct page opening failed. They are firsthand accounts, not representative research, current usability tests or analytics.

## Predictive direction: standards supported by primary sources

[Kovalchik 2016](https://vuir.vu.edu.au/34652/1/jqas-2015-0059.pdf) evaluates eleven approaches on 2,395 ATP matches from 2014, with bookmaker benchmarks and substantial differences across rank groups. Simple ranking regressions and Elo are strong. It supports baseline/subgroup scrutiny, not a current betting edge.

[Vaughan Williams, Liu and Gerrard 2019](https://www.ntu.ac.uk/__data/assets/pdf_file/0024/830562/how-well-do-elo-based-ratings-predict-professional-tennis-matches.pdf) evaluates Wimbledon 2018; bookmaker odds lead men's accuracy and calibration. A single tournament does not establish universal superiority.

[Official scikit-learn calibration documentation](https://scikit-learn.org/stable/modules/calibration.html) distinguishes reliability diagrams from overall proper scores and warns about fitting/calibrating on the same samples. A better Brier or log-loss score alone does not establish better calibration. For this project's report, show calibration bins and independent match counts, keep chronological boundaries, and label repeatedly inspected 2025 as retrospective rather than pristine prospective validation.

## Consequential recommendation, still a hypothesis

The strongest supported first experiment is a short, authored match investigation using the RG25 point sequence. The portfolio value would come from information design, animation that preserves meaning, a coherent interaction and visible data judgment. Model sophistication is optional. The main challenge is turning one compelling specimen into a repeatable editorial form without manufacturing explanations.

Cheap falsification: give five people the uncoached specimen and a second unopened case. Observe first action and time to first discovery; ask them to explain why more total points did not mean victory, then offer no prompt to continue. A provisional pass is at least four correct explanations and at least three voluntary second-case opens. Record confusion, not just favorable comments. This tests comprehension and short-session curiosity, not retention or demand. A separate visual review should judge hierarchy, type legibility, continuity of marks, purposeful motion and coherence at desktop/mobile sizes. No participant testing occurred in this investigation.
