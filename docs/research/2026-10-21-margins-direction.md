# Margins: agreed product direction and proposed next experiment

2026-10-21. Records the user's agreed direction after implementation/data investigation. The user accepted Wimbledon 2019 and its argument as strong enough if the interaction makes it feel surprising. After the original **“Don't build yet”** discovery/planning phases, the user explicitly authorized the bounded disposable experiment. It now exists at [gui/margins-experiment](../../gui/margins-experiment/index.html); [verification and limits](2026-10-21-margins-experiment-verification.md) record the result. Production integration, publishing, recruiting and scheduling remain unrequested.

The subsequent [design and motion specification](2026-10-21-margins-design-motion-spec.md) develops one bounded sequence, assigns distinct responsibilities to the newly available skills, and defines independent evidence, observation, browser and visual acceptance checks. It supersedes the tentative choreography below, while preserving the direction and exclusions. The [independent score-state audit](2026-10-21-motion-evidence-audit.md) records specimen conventions and verification limits. The remainder of this brief records the decisions and proposed experiment before implementation; use the verification note for its current execution state.

## The work

**One finished, authored historical tennis investigation for statistically minded fans who already know the match.** It tests a familiar narrative, earns a clear verdict and lets readers inspect or challenge the evidence. The desired reaction is: “I know this match, but I had not understood that.”

The user explicitly chose niche over accessibility to tennis-unfamiliar portfolio reviewers. Basic scoring explanations, familiar point totals and famous match-point clips are insufficient as the analytical payoff. Enjoyment of implementation is not a selection criterion; usefulness is a bonus. No regular updates or continuing publication are promised.

## Defining experience and visual identity

An arresting claim leads into one dominant visual stage. As the argument develops, the same point records change arrangement: aggregate → match phases → selected evidence. Motion reveals relationships and preserves identity. The reader can stop the sequence, examine its cuts, restore the full context and then resume the authored argument. Inspection must be substantive, not simply a citations link.

The user chose **dramatic sports editorial**: oversized sporting typography, strong contrast, bold scale changes, sharply paced reveals and memorable motion tied to the evidence. Precision remains visible through stable player encoding, clear denominators, score/date labels and direct comparison controls. Typography, composition and purposeful movement carry the visual signature. The earlier quiet serif-and-dot study is evidence of technical feasibility, not the accepted final design.

The narrative has a deliberate ending: a bounded verdict, what the records establish, what they do not, and an invitation to challenge the reasoning using the same evidence. No endless dashboard or content feed.

## Selected specimen: Wimbledon 2019 men's final

Selected question: **“How much of Federer's statistical advantage was sustained across the final?”** A possible opening is “Fourteen points ahead. Where did the advantage come from?” The exact headline remains an execution choice; avoid “illusion” or “robbery,” which would prejudge the evidence. The user accepts the argument's potential on the condition that the interaction makes it feel surprising. That is a design requirement, not evidence that the interaction has succeeded.

The fresh point probe retrieves 422 unique records, numeric points 1–422, from the original public [Match Charting Project point file](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-points-2010s.csv). Charted by Zindaras. Results agree exactly with the local ATP row (`2019-540`, match 226). [Actual source report](https://www.tennisabstract.com/charting/20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic.html).

| Set | Federer points | Djokovic points | Federer margin |
|---|---:|---:|---:|
| 1 | 41 | 46 | −5 |
| 2 | 26 | 12 | +14 |
| 3 | 37 | 36 | +1 |
| 4 | 30 | 25 | +5 |
| 5 | 84 | 85 | −1 |
| All | 218 | 204 | +14 |

**Verified finding:** all of the net 14-point advantage is accounted for by the second set's 26–12 margin. The other four sets' 384 points split 192–192. The second set contains 38 of 422 points, about 9%. The three tiebreaks split 12–21 in Djokovic's favor.

**Bounded verdict:** Federer's total-point advantage was real and concentrated. The full-match total alone does not establish sustained dominance across the final. This does not erase the second set, make it unimportant, or establish equal performance in every other phase. It does not prove either player's intentions, mental strength, choking, or the cause of the result.

This is **not a new statistical discovery**. A [contemporary July 2019 analysis](https://www.deconstructingtennis.com/blog/wimbledon-mens-final-analysis-2019/) already notes the 192–192 split outside set two. [Sackmann's July 2019 analysis](https://www.tennisabstract.com/blog/2019/07/26/roger-federer-wasnt-clutch-but-he-was-almost-clutch-enough/) already goes beyond the familiar match points to modeled leverage and argues that Federer's high-leverage performance was less poor than memorable moments suggest. Its leverage values have not been reproduced here. A distinctive interaction can make a documented result newly understandable to a particular reader; whether that surprises knowledgeable fans must be tested.

Do not animate removing the second set as if the match would otherwise have played identically. Isolating the set is a descriptive partition. Keep the full-match total visible or immediately recoverable and label the selected sample. The verdict must acknowledge the strongest objection: the second set counted and Federer genuinely won it decisively.

## First 30 seconds to test

1. A large 218–204 count and a provocative, answerable question establish the familiar narrative.
2. The reader commits a rough expectation about where the 14-point margin accumulated, or directly advances if the extra commitment proves obstructive.
3. The same 422 points split into five phase contributions. The second set's +14 dominates; the other four contributions net to zero. The reader can isolate and restore it.

This first beat needs to earn further exploration. The next beat should examine score context and the limits of the aggregate without claiming a psychological explanation. Full-match data inspection and counterargument remain available. One small segment is enough for the next experiment; a complete multi-chapter production is not yet warranted.

## Explicit exclusions

- Betting, bookmaker comparison, ROI, forecasts and live/current-season services.
- Accounts, leaderboards, broad player search, generalized scouting, a universal tennis dashboard or a publishing schedule.
- A multi-case minimum, content feed or requirement to open a second case.
- Simulated physical ball trajectories, unlicensed match footage, video synchronization or invented shot locations.
- Automatic causal/tactical/mental-strength claims, unvalidated live win-probability curves and unlabeled counterfactuals.
- An original-research claim merely because an old finding is presented in a new interaction.

These boundaries define the chosen work and keep it within the investigated evidence. They do not authorize implementation.

## Proposed smallest next experiment

**One disposable, polished 60–90 second evidence sequence for this candidate case.** It should establish the question, reveal the concentration, allow isolate/restore/challenge, and end with the bounded verdict. Implement only the central interaction, with desktop/phone and reduced-motion paths. No production backend or wider site.

When the user requests the experiment, test with five statistically minded tennis fans who know the final. Before showing the sequence, record their existing account of the match and familiarity with the 192–192 result so the test cannot manufacture surprise. Knowing the number does not disqualify a participant: the interaction can still make its implications newly understandable. Do not recruit or send messages without user authorization. No participant work is currently underway.

Provisional success criteria:

- At least four operate the reveal and inspection controls without coaching.
- At least three articulate a specific new or materially sharpened understanding of the match, substantiate it from the displayed records, and identify which transformation or comparison made it clear. A restated headline or praise for animation does not count. Compare against their baseline account; numerical novelty is not required.
- At least three voluntarily inspect another evidence cut or the counterargument after the reveal, without a request to do so. Completion or compliments alone do not count.
- At least four understand that isolating set two does not prove its points were unimportant or that the remaining match would have played the same way.

Visual review should identify whether the headline has primacy, motion preserves evidence identity, labels/denominators remain legible, and the inspection mode stays coherent with the dramatic editorial. Favor specific defects over “looks cool” ratings. Passing this small test supports the segment, not demand, novelty or retention. Failure should trigger a better claim or interaction, not extra features.

## Reproduction and current state

`python docs/research/wimbledon_case_probe.py` recomputes the ledger from the retained ignored subset. `--fetch` retrieves the public source specimen when network access is available. Subset SHA-256: `b772afeb9e76baa3f0c7c21c0351ae72dddfcf47afe2111378b6bfeb720e89f3`. Outputs: ignored `reports/discovery/wimbledon2019-final-points.json` and `wimbledon2019-ledger.json`. No credentials/key/account needed. Preserve MCP attribution and CC BY-NC-SA 4.0; publication-specific rights remain a pre-publication issue.

Base commit remains `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`; unrelated deletions/untracked implementation preserved. Production code, source CSVs, models and dependency declarations are unchanged. No new visual study has been built for this specimen. Next action is deferred until the user explicitly asks to proceed. No further interview question is required to settle the direction; exact headline, choreography and inspection controls belong to the bounded next experiment.
