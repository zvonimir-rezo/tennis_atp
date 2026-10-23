# Margins: one evidence transformation

2026-10-21. Design and motion specification only. No implementation, dependency installation, new visual prototype, recruitment or publication. This develops the [settled brief](2026-10-21-margins-direction.md), not a new direction search. Current commit: `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`.

## Recommendation

Lead with **Impeccable's shape workflow**, using Experience for the dominant visual stage, Read for the argument and Operate for inspection. Establish the evidence contract, design the still compositions, then specify one reversible transformation. Use Taste as a bounded composition critic, Animate and Emil as implementation guidance, and animation review as a later independent check. Do not run every skill's complete workflow.

The defining experience is **a ledger that changes arrangement without changing history**. All 422 point records persist as the reader moves from the familiar 218–204 total to five set contributions, holds set two's 38 records apart, and sees the other 384 split 192–192. The work then exposes the objection and a fuller partition before delivering its verdict. Bold editorial framing and precise conservation of evidence must reinforce each other.

The hardest assumption is perceptual and argumentative: can a knowledgeable reader understand the rearrangement as an illuminating partition, rather than decorative sorting or selective deletion? That is the experiment's primary risk. No claim of appeal, novelty or superior comprehension has been established.

## Evidence contract, independently checked

The [independent audit](2026-10-21-motion-evidence-audit.md) recounts the retained original-format MCP specimen and independently replays every pre-point score and server, without calling the existing probe. Retained file: `reports/discovery/wimbledon2019-final-points.json`; SHA-256 `b772afeb9e76baa3f0c7c21c0351ae72dddfcf47afe2111378b6bfeb720e89f3`. Canonical record identity is `(20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic, Pt)`, never a screen coordinate.

| Group | Inclusive point IDs | n | Federer | Djokovic | Federer margin |
|---|---|---:|---:|---:|---:|
| Whole match | 1–422 | 422 | 218 | 204 | +14 |
| Set 1 | 1–87 | 87 | 41 | 46 | −5 |
| Set 2 | 88–125 | 38 | 26 | 12 | +14 |
| Set 3 | 126–198 | 73 | 37 | 36 | +1 |
| Set 4 | 199–253 | 55 | 30 | 25 | +5 |
| Set 5 | 254–422 | 169 | 84 | 85 | −1 |
| Other four sets | complement of 88–125 | 384 | 192 | 192 | 0 |
| Three tiebreaks | 76–87; 188–198; 413–422 | 33 | 12 | 21 | −9 |
| Neither set two nor a tiebreak | complement of both groups | 351 | 180 | 171 | +9 |

Thus **38 + 33 + 351 = 422**, and **+14 − 9 + 9 = +14**. These last three groups are disjoint. The set-two share is 38/422, about 9%; the claim concerns its net surplus, not a claim that every other phase was equal.

The [original match report](https://www.tennisabstract.com/charting/20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic.html) credits charting to Zindaras. The [MCP dictionary](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/data_dictionary.txt) and [README](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/README.md) distinguish charted input from generated fields. Important specimen-specific checks:

- Player 1 is Federer, the first server. `Set1/2` and `Gm1/2` use player identity. `Pts` is **pre-point and server-relative**, established by replay. Point 81 has Djokovic serving at raw `3-2`: display Federer 2 / Djokovic 3 in a fixed player-order interface.
- `TbSet` says the set permits a tiebreak; it does not identify tiebreak points. Infer this match's membership from verified score states. The fifth-set breaker began at **12–12**, first to seven with a two-point lead.
- Points **359 and 360** begin at Federer serving, sets 2–2, games Federer 8–7, **40–15 and 40–30**. Djokovic wins both. They are championship points outside the tiebreak group. A “tiebreaks = all pressure” label would be false.
- Final score from Federer’s perspective is 6–7, 6–1, 6–7, 6–4, 12–13; Djokovic wins three sets to two. Federer also won 36 games to 32. These are available to challenge a narrow reading of point equality.
- No per-point timestamps, physical coordinates or psychological measurements exist. Point ordinal is not elapsed time. Do not invent ball flights, match-time spacing or mental states.

Local ATP aggregate arithmetic independently reconciles 218/204 and 422 using a different record structure. Both sources are maintained by Sackmann, so this does **not** establish independent collection. The [official score sheet](https://www.wimbledon.com/en_GB/scores/2019/schedule/pdf/schedulePDF21.pdf) corroborates the result; the [ITF account](https://www.itftennis.com/en/news-and-media/articles/djokovic-beats-federer-in-epic-wimbledon-final/) corroborates the 14-point margin and famous score states. Fresh retrieval of the large upstream CSV failed through available network/fetch paths this turn; the retained specimen, not today's upstream revision, is the verified input. Dictionary and report access succeeded. Preserve the frozen subset and provenance; no live dependency is needed. MCP attribution and CC BY-NC-SA 4.0 remain publication constraints.

**Claim:** Federer's point advantage was real and concentrated; the full-match total alone does not establish sustained dominance.

**Strongest objection:** Set two counted. Its 26–12 split represents real dominance in a real set. Equal totals elsewhere do not imply equal playing quality or equality at every score state. Federer’s game advantage is further context, not an inconvenient statistic to hide.

**Limit:** This descriptive partition cannot establish who deserved the title, why a player made a decision, whether either choked, or what would have happened without set two. It is not an evaluated model of leverage or a causal explanation.

**Prior art:** [Bob Schewior's July 2019 analysis](https://www.deconstructingtennis.com/blog/wimbledon-mens-final-analysis-2019/) already states 192–192 outside set two. [Sackmann's contemporary leverage analysis](https://www.tennisabstract.com/blog/2019/07/26/roger-federer-wasnt-clutch-but-he-was-almost-clutch-enough/) goes beyond the famous failures; its modeled values have not been reproduced here. A [previous visual essay on the same final](https://medium.com/nightingale/why-the-2019-wimbledon-mens-final-is-one-to-be-remembered-175549d2109a) also exists; only its opening was accessible. Credit the finding and claim originality only for the eventual expression if justified.

## Workflow and actual tool fit

The named skills' actual files were inspected, including supporting motion/type/adaptation guidance and review standards. These are distinct responsibilities, not an instruction to execute all commands.

| Tool or guidance | Responsibility here | Important constraint or conflict |
|---|---|---|
| [Impeccable](../../../../.agents/skills/impeccable/SKILL.md), v4.7.0 | Lead: shape one experience, establish information hierarchy and mode changes, then judge complete compositions. Its animate/type/adapt guidance supports the spec. | Its workflow-advice route allows advice without commands. Do not initialize a new project, roll concepts, generate alternatives or repeat the settled interview. User's planning-only scope overrides build/interview gates. Existing bundled binary was inspected, not executed. |
| [Taste](../../../../.codex/plugins/cache/taste-skill/taste-skill/2.1.4/skills/taste-skill/SKILL.md), v2 | Subject-specific art direction and later screenshot critique: does this look authored around this particular argument? | Skip random direction dealing, image floors, moving-element quotas and blanket bans on analytical labeling. They would manufacture material and motion. No need for four photos or eight-plus moving ornaments. Its Chrome inspection script can measure screenshots, overflow, fonts and contrast; it does not by itself exercise all narrative states, measure frame delivery or prove appeal. |
| [Animate](../../../../.agents/skills/animate/SKILL.md) | Specify purpose, property, tool, duration, easing, exit and interruption for the one focal transition; later implement only when requested. | It normally writes code. No code now. Generic sub-300ms rules apply to repeated controls, not every explanatory transformation. Its keyboard-animation ban assumes frequent shortcuts; deliberate keyboard Replay must retain equivalent educational access. |
| [Emil](../../../../.agents/skills/emil-design-eng/SKILL.md) | Detail discipline: instant direct manipulation, interruptibility, consistent controls, touch, reduced motion and hidden-tab behavior. | Avoid springs, inertia and blur on evidence. “Feels alive” cannot alter quantitative positions or obscure record identity. |
| [Review animations](../../../../.agents/skills/review-animations/SKILL.md) and its standards | Later independent code review of the implemented transition and exceptions: concrete defect, fix and reason. | No implementation exists to approve. Review cannot certify comprehension, aesthetic quality or measured runtime from code alone. |
| [Improve animations](../../../../.agents/skills/improve-animations/SKILL.md) / [find opportunities](../../../../.agents/skills/find-animation-opportunities/SKILL.md) | No broad audit now; their purpose/frequency gates reinforce choosing one move. | Auditing the old GUI for opportunities is unrelated work. Do not generate a roadmap or opportunistic animations. |

Relative skill links above resolve outside the repo; actual local locations were checked. The current brief overrides contradictory generic house rules. In particular, prefer literal sample labels and a readable record index over a marketing-only prohibition on labels, and genuine evidence continuity over minimum motion counts. Transform/opacity recommendations are performance hypotheses: SVG updates are not automatically compositor-only.

**Available supporting capabilities:** CUA has been used for actual reference interaction. Available Chrome DevTools tools support viewport/CPU/reduced-motion emulation, screenshots, recordings and performance traces; they have not been used to certify a Margins implementation. Node 24 and Chrome are already present. No additional plugin is necessary. Sites would introduce hosting rather than solve the interaction; ImageGen cannot be the source of exact point evidence; neither is part of this workflow. No install, account or paid usage is proposed.

Future order, confined to this work: freeze and verify evidence → draw endpoint and intermediate compositions → implement the single motion contract → observe the small experiment → separately inspect visual craft, code motion and measured browser behavior. A failure at the argument stage should not trigger more decoration.

## Original experiences actually exercised

**[The Pudding: Pockets](https://pudding.cool/2018/08/pockets/).** Selecting iPhone X produced the displayed 40% women's / 100% men's fit comparison; selecting Pen changed it to 98% / 100%. The pocket outlines remain a concrete measurement frame while the selected object and fit state change. The transferable mechanism is *selection with preserved context*: the reader sees what changed and what the denominator still means. Margins should preserve point membership, player encoding and the full-match summary while changing the partition. Its imagery, palette and long page are not the recommendation. Endpoints and visual changes were observed; transition durations were not instrumented.

**[Nicky Case: The Evolution of Trust](https://ncase.me/trust/).** Played the opening interaction through CHEAT: the machine/payoff highlight and subsequent explanation make the chosen action legible before advancing the argument. The useful mechanism is *act → visible consequence → authored interpretation*. Margins can ask a deliberate action, show where the records went, then state its bounded conclusion. Do not borrow its cartoon style, sound, long simulation or forced pacing. Only the opening exercise was played, not the entire work; local duration and attention effects are unmeasured.

R2D3's original machine-learning introduction returned a 522 error. It is excluded from interaction evidence rather than treated as inspected from memory. Two working references are sufficient; neither validates this proposed experience with expert tennis fans.

## Storyboard: approximately 80 seconds, paced by the reader

This is a target observation window, not an autoplay clock or time gate. Native document scrolling remains available. A single evidence stage changes state through explicit controls; no scroll hijacking. Back, Pause during movement, and Evidence remain discoverable. The reader can take longer or skip motion.

| Time | Initial belief / question | Reader action | Composition and change | Defensible discovery |
|---|---|---|---|---|
| 0–12 s | “Federer won more points; perhaps that advantage ran through the final.” | Read, then **Trace the margin**. No quiz required. | Huge **FOURTEEN AHEAD.**; beneath, “Where did the advantage accumulate?” Federer **218**, Djokovic **204** over two equal-unit fields containing all 422 marks. Context: Wimbledon final · 14 July 2019 · Djokovic won 3–2 sets. A smaller full score and provenance are accessible. | Establishes a familiar fact and an open distributional question. Does not assert the reader held a naive belief. |
| 12–28 s | “Was the surplus spread across the match?” | Advance or pause; select a set label if desired. | The same marks reorganize into five chronological set bands. Each has Federer/Djokovic totals, `n`, final game score and signed Federer margin **−5 / +14 / +1 / +5 / −1**. Large +14 anchors set two; others retain equal label size and clear denominators. | Different phases contributed differently; the other four net to zero, despite individually unequal sets. |
| 28–46 s | “How can one phase account for the full margin?” | **Hold set two apart**; optionally reverse. | The 38 records from IDs 88–125 travel into a visible compartment labeled **Set 2 · 38/422 · 26–12**. The remaining 384 settle into equal fields labeled **Other four sets · 384/422 · 192–192**. All marks remain, and the global 218–204 / 422 summary stays visible. Text: “The entire net surplus sits here.” | Concentration becomes inspectable as conservation, not a new match with evidence removed. |
| 46–65 s | “But set two counted—and the other sets were not uniform.” | **But set two counted**; then optionally inspect a group. | Restore the full ledger into three disjoint compartments: **Set 2: 38, 26–12, +14**; **Three tiebreaks: 33, 12–21, −9**; **Remaining points: 351, 180–171, +9**. Equation **+14 − 9 + 9 = +14**. The objection is normal editorial text, not a hidden disclaimer. | Even the 192–192 remainder contains contrasting distributions. Tiebreaks explain a partition, not all high-pressure play or psychology. |
| 65–85 s | “What does this actually settle?” | Read verdict; voluntarily open evidence or challenge, or finish. | **A REAL ADVANTAGE. CONCENTRATED.** The three-part ledger remains alongside/below the bounded verdict. “The full-match point total alone does not establish sustained dominance.” Direct challenge text: “Set two was real. Federer also won more games. Equal totals do not mean equal quality.” Evidence controls stay live. | A specific limit on the familiar statistic, with enough access to disagree. No claim about deservedness or nerves. |

No numerical count-up, artificial score-clock, fireworks or trophy reveal. Numbers change only when the corresponding named partition becomes the active settled state; total 422 never changes. During a transition, retain source labels and a literal “rearranging the same records” state rather than presenting an interpolated count as data.

## Compositions and identity

**Visual identity:** cold ink `#101411`, paper `#F2F3EE`, acid lime `#C8F44A`. Federer is a paper circle; Djokovic an equal-area lime square. Repeat names and shape keys: color alone is insufficient. Selection uses a bracket/outline and a named sample label, never a new winner color. Proposed palette contrast must be measured in rendered states before acceptance.

Proposed typography is **Barlow Condensed 800** for compressed sporting headlines and large verdicts, with **Inter 400/600** for argument, evidence labels and tabular numerals. Barlow Condensed's [official font repository/license](https://github.com/google/fonts/blob/main/ofl/barlowcondensed/OFL.txt) is available; no font was downloaded now. An eventual self-hosted licensed font asset is sufficient. No new font library is needed. The existing quiet serif prototype is not a source of design authority.

Desktop: one dominant field, not a dashboard grid. Headline roughly 112–160px, primary counts 64–88px, body 18px with a 55–70-character line, labels 16px. Two player lanes maintain left/right order. Set layouts run top-to-bottom chronologically; within each winner/group marks are ordered by point ID, making the geometric ordering explicit rather than implying a literal court or time axis. Equal-size cells, equal-area shapes and direct totals prevent visual area tricks. Typography can be enormous because the evidence hierarchy remains stable underneath it.

Essential intermediate: set two's selected records are bracketed **before** travelling; its source band remains labeled while the destination compartment becomes visible. Readers need to track the selected group and a focused record, not individually memorize 422 trajectories. Keep the two endpoints recognizable through the move, and do not animate type scaling or a camera zoom that loses context. The ending uses the same player encoding, record marks and summary strip, with a stronger sentence rather than a different visual system.

**Phone is a separate arrangement.** At 390px, use a 56–72px headline, 40–48px counts, 17–18px body and labels at least 14px. Five set bands stack vertically with paired player lanes; set two's compartment sits above the balanced 384. The challenge's three groups stack instead of becoming miniature columns. A stage around 540–660px high is a starting composition to test, not a fixed requirement that clips text. All 422 marks exist without horizontal panning or virtualization; it is acceptable for the document to scroll. A roughly 6–7px grid pitch is plausible but unverified. Marks are not 422 tiny touch buttons.

Use full-width named group controls and a compact record panel below the selected group. Controls have at least 44px touch areas; no hover-dependent meaning. A small persistent summary/Back/Next area may stay in view only if it does not consume the chart. No app-style bottom navigation. Resize/orientation changes pause the transition, recompute the composition and settle at a named endpoint while retaining the selected record.

## Inspection and challenge

- **Pause/reverse:** Pause freezes the narrative playhead. Back can reverse the current edge from its current pose; replay is explicit. State labels describe settled arrangements, not a fictitious half-selected dataset.
- **Inspect a subset:** activate Set 2, Three tiebreaks, or Remaining points. Show both `n/422` and winner counts; the selected IDs remain visibly bounded while context retains normal-readable labels. No disappearance or denominator renormalization. Restore all has one predictable action.
- **Inspect a record:** a focused point has its ID, named server, normalized pre-point sets/games/points, winner and optional literal charting plus definitions/source. Use a single keyboard entry into the visualization and point stepping or a semantic table; do not create 422 sequential tab stops. Hover may preview, but click/touch/keyboard can pin the same record. Escape closes the panel and returns focus to its trigger.
- **Challenge:** the explicit objection restores all 422 and exposes the disjoint partition. The record panel includes direct examples 359/360 to demonstrate that tiebreaks do not exhaust consequential score states. Show the 36–32 game count in the objection context. Do not add a general filter builder or live leverage model.
- **Context recovery:** preserve the selected record key when changing arrangements; show its destination and new group's denominator. Restoring context never silently clears the user's point or changes player orientation. If inspection is requested mid-motion, settle to its named destination before presenting the exact static panel; acknowledge the request immediately.

## Motion contract

Movement contributes **visible provenance across arrangements**: the 38 points are held apart while the complementary 384 remain. Static panels can prove the arithmetic; motion may reduce the mental matching required to see it as one conserved ledger. That additional benefit is a hypothesis to test, not a reason to force every reader through animation.

| Purpose | Proposed timing and curve | Behavior |
|---|---|---|
| First deliberate whole → five sets | 760ms, `cubic-bezier(.77,0,.175,1)`; optional offsets of 40ms across five groups, total no more than 920ms | Shared playhead; legible departure, transfer and arrival. No per-point 422-item stagger. |
| Hold set two apart / fuller partition | About 800ms, same curve | No overshoot or inertia. Selected group bracket remains continuous. Pause and reverse available. |
| Repeated subset selection and point stepping | Immediate geometry/state; at most 120ms opacity feedback | Inspection prioritizes response. Never replay the authored rearrangement on each click or arrow press. |
| Button acknowledgment | 100–120ms, `cubic-bezier(.23,1,.32,1)` | Focus itself is immediate and persistent. No hover movement that changes the hit target. |
| Record panel | 160–200ms entry; 120ms exit, same ease-out | Modest opacity/translation only if useful; no blurred text. Panel content and focus are available immediately. |
| Reduced motion | No spatial travel; stable endpoint comparison with explicit brackets and labels; optional 80–100ms opacity feedback | Same evidence, controls, denominators and conclusion. Change preference live as well as on load. |

One active controller owns the playhead. Latest requested target wins; no transition queue or stale completion callback. Retarget from the actual current pose when possible, not from a reset origin. Reverse follows the existing trajectory. Direct point manipulation is immediate. Deliberate keyboard activation of Replay gets the same explanation as pointer activation; routine keyboard navigation never triggers decorative motion. Pause when the tab is hidden and require explicit resume. Reduced-motion activation settles safely and retains selection. Do not equate display-frame interpolation with intermediate analytical states.

## Smallest implementation, when requested

The project already supports plain HTML/CSS/JavaScript. Use semantic HTML for argument/controls/table and one **SVG with 422 persistent keyed marks**, plus a small vanilla state controller. Use native **Web Animations API** for coordinated playhead, pause, reverse and cancellation; CSS suffices for control feedback. [MDN's API documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API) supports those controls. A single controller can update matching animations; verify their behavior in the target browsers rather than assuming ideal SVG compositing.

Prepare one frozen JSON using Python standard library and existing records. Derive totals from immutable ID sets; animation only changes coordinates. Keep chapter, layout, selection, focused record, playhead and motion preference separate. Pure layout functions produce coordinates for each ID on each viewport. No React, D3, GSAP, Motion, Canvas, WebGL, backend or new package is justified by 422 marks and this interaction. The [browser performance guidance](https://web.dev/articles/animations-guide) favors avoiding unnecessary layout/paint and measuring actual behavior; do not promote hundreds of layers with blanket `will-change`.

## Experiment and acceptance before implementation

The proposed next experiment is exactly the above sequence, with final-quality type/hierarchy and honest data, not a production site. Nothing has been built or tested with participants. Do not recruit or send messages until authorized.

### Independent evidence checks

Use a separate oracle/recount rather than testing production helpers against themselves. Verify the SHA, 422 unique IDs, original winner identity, per-set counts, subset complements and disjoint union. Independently replay pre-point scores and service, including points 76/81/87, 88/125, 188/198, 359/360 and 413/422. At every settled layout, compare displayed counts and represented IDs to the oracle. At intermediate frames check every record exists exactly once and retains winner/identity; labels must not pretend interpolation is a new sample. Verify identical semantics through reverse, interrupted selection, restore, phone reflow and reduced motion. Any record, score-orientation or denominator error blocks acceptance regardless of appearance.

### Five knowledgeable tennis fans, uncoached

Before exposure, record each person's existing account of the final, interpretation of 218–204, familiarity with the second-set finding and confidence. Do not seed the 192–192 answer. Knowing the result does not disqualify someone. Give a neutral task: “Explore this investigation as you normally would.” Record first action, hesitation, mistaken inference, completion time, pauses/reversals, and any voluntary post-reveal inspection before asking questions.

Provisional support requires all of:

- **4/5** operate reveal and inspection without coaching.
- **3/5** articulate a specific new or materially sharpened understanding versus their baseline, substantiate it using the evidence and identify the comparison that clarified it. A new number, repeated headline or compliment does not count.
- **3/5** voluntarily inspect a record, another group or the counterargument after the reveal. Clicking the required next step does not count.
- **4/5** understand the limits: set two counted; equality outside it is aggregate; this does not establish equal quality or mental strength.

Reject the present treatment if two or more interpret isolation as discarding evidence, fewer than three gain substantive understanding, or the reveal consistently produces only “I already knew the tiebreak story.” Revise the argument or interaction rather than expanding scope. An optional static counterpart can diagnose whether motion helps identity matching; five qualitative sessions cannot establish statistical superiority of animation, market demand or retention.

### Browser and runtime checks

Test desktop 1440×900, tablet 768×1024, phones 390×844 and 360×800, plus a 320px/200%-zoom overflow check. Exercise Tab, Enter, Space, point-step arrows and Escape; touch equivalents; load-time and live reduced motion; interruptions at 10/50/90%; five rapid direction changes; hidden-tab pause/resume; resize; font fallback; and readable content without JavaScript. Record identity and focus must survive, and all argument content must remain accessible.

**Targets, not measured results:** readable text LCP ≤2.5s; CLS ≤0.1; control acknowledgment ≤100ms; aim for at least 95% of frames within a 16.7ms budget on a specified 60Hz target device, with no >50ms stalls during the focal move. Inspect actual frame delivery and paint in traces, not only `requestAnimationFrame` averages. Collect three cold/warm runs with viewport, browser, device and CPU conditions recorded. Use 4× CPU emulation as a stress diagnostic and a physical midrange phone for mobile judgment; neither substitutes for the other. If SVG misses the budget, simplify paths/stagger/layout first; do not assume a renderer rewrite is required. No performance measurement has occurred yet.

### Separate visual critique

Review still endpoints, representative intermediate frames and real playback before anchoring on automated scores. Judge one focal hierarchy, expressive but readable type, stable player meaning, equal units, continuity of the selected 38, legible opposition and a phone composition with its own rhythm. Ask whether the +14 is first understood in relation to the other four margins, and whether the ending feels earned rather than like a disclaimer after a trick.

Measured defects include clipping, wrong labels/counts, focus loss, overflow, insufficient contrast (4.5:1 ordinary text, 3:1 large text and essential graphics), tiny controls and trace stalls. Aesthetic judgments include whether the headline has enough sporting force, the motion has tension, or the acid accent feels coherent. Record reasons and disagreements; an award-style score or skill detector pass is not evidence of fan insight. A visually excellent sequence still fails if its argument misleads or nobody chooses to inspect it.

## What makes this particular work distinctive

The known statistic becomes an object the reader can take apart without losing its records. The objection is part of the climax, not an appendix. The apparently even remainder is reopened into −9/+9 components, and the famous championship points demonstrate the limits of a tiebreak-only story. Large sporting type supplies drama while the preserved ledger supplies trust. Whether that combination feels memorable or surprising remains the explicit experiment—not a premise used to justify a larger product.
