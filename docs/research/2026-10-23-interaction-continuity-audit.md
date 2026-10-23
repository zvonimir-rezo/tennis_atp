# Interaction continuity audit — 23 October 2026

Historical comparison. The [final reader pass](2026-10-23-final-reader-pass.md) now resolves all four findings and makes the readable sequence the default. The two URLs below now show the same finished experience. Original prototype sources remain in `reports/discovery/final-pass/before/`; before/after recordings preserve the comparison. The implementation and status statements below describe the audit checkpoint.

The shot sequence feels like slides because each input replaces the current explanation and diagram while the visible selector offers only numbers. The reader gets a succession of facts, but little durable structure for comparing them. More transition choreography would prolong this memory task. The bounded prototype tests a persistent, readable record in the existing selector, with immediate court updates.

Scope: the existing tactical demo’s opening → court split → results → service-point objection → three pressure moments → full-game challenge → verdict → sources; also the linked Wimbledon study, as an existing example of persistent evidence under scroll. No case, data, feature, animation library, reusable system or redesign was added. The normal tactical URL retains the current behavior. These findings combine implementation inspection, primary source checks, scripted recordings, native in-app-browser use and Chrome measurements. They are a single-designer assessment, not an independent human usability study.

## Prioritized findings

### 1. High: shot inspection erases the comparison the reader needs

**Reader’s task.** Understand how the five strokes at set point contain two backhand volleys, and why the two-stroke next serve needs no volley. Compare specific strokes without memorizing the last screen.

**Observed behavior.** `pressure-shots.js` updates the title, detail, token and categorical court together, then rebuilds every numbered selector button on each step. At point 154, all 13 buttons are replaced even when only the selected stroke changes. Visible buttons say 1–13; their useful actor/stroke names exist only in accessibility labels. Earlier facts disappear from the visible explanation. The court’s geometry correctly avoids a replay, so it cannot supply the missing temporal context. DOM replacement alone does not explain perception; the more consequential absence is a readable sequence.

**Persist / respond.** Keep player identities, schematic ends and the ordered record visible. Move selection directly with input. Change the current category and explanation immediately. Earlier tokens must remain identifiable without implying an elapsed duration, contact position or path.

**Smallest intervention — prototyped.** Reuse the existing selector as a horizontal sequence of player/stroke/source-fragment buttons above the court. Keep those nodes while inspecting one point; change only selection. Retain previous/next, ending shortcut and Arrow/Home/End input. Reveal the selected tile within its own scroll container, without scrolling the page or adding a tween. One Tab stop enters the selector; Tab exits it. The header identifies the source point.

**Verification.** All 20 source fragments and alternating actors agree with the original strings. Same-point input retains 13/13 controls instead of 0/13. A 28-selection stress run removes 0 selector nodes instead of 364. Keyboard, boundaries, rapid reversal and reduced motion pass. These demonstrate inspectability and control. Whether readers notice and explain the two volleys more readily remains an audience question.

Code: [current renderer](../../gui/margins-experiment/tactical-demo/pressure-shots.js), [bounded alternative](../../reports/discovery/final-pass/before/continuity-prototype.js).

### 2. High: challenging the edit removes the reader’s place

**Reader’s task.** Examine all 14 points, especially the double faults omitted from the three illustrated sequences, and return to the edited argument.

**Observed behavior.** Selecting source point 146 hides the entire shot figure because that point has no audited stroke sequence. The disclosure and its point controls sit below that figure, so they move upward while scroll position stays fixed. At 1440×900 the selected button moves from y=428 to y=−426; at 390×844 from y=400 to y=−412. Both leave the viewport. The narrower layout also separates the moment controls above the figure from the commentary below it. Reopening a pressure moment starts its stroke sequence at the serve; a visit to an ending is not retained.

**Persist / respond.** The selected point, navigation, source identity and inspection frame should remain in a stable place. Unsupported shot information must stay explicitly unavailable. Revisiting a moment should either preserve the inspected stroke or make the restart clear; that choice needs reader observation.

**Smallest intervention.** Keep the existing figure’s inspection space when a non-illustrated point is selected, with a plain statement that no shot view was prepared for that point and access to its real result/record. Preserve the point control’s viewport position. Do not fill the gap with invented court action. This is a proposed correction, not part of the one prototype.

**Verification.** Open the full game; select 146, 148, then 150 using pointer and keyboard. The active control and selected-point identity should remain visible, focus should remain usable, and no unsupported strokes should appear. Ask a reader to inspect a double fault and return to the second volley without guidance. Use the current recorded displacement as the regression case.

Code: `pressure-shots.js:88`, tactical `index.html` figure/disclosure order, and `demo.js:135–163`. Evidence: [before/after geometry](../../reports/discovery/interaction-audit/journey-check.json), [phone before](../../reports/discovery/interaction-audit/challenge-390-before.png), [phone after](../../reports/discovery/interaction-audit/challenge-390-after.png).

### 3. Medium: the scroll handoff invites input before it is possible

**Reader’s task.** Follow the same court as it opens into categories, then inspect those categories.

**Observed behavior.** Crossing progress .4 changes the editorial mode abruptly: at desktop width the headline top jumps 153→45 px and its height changes 302→164 px. On the phone it jumps 135→30 px. The copy already says to open each group, but evidence remains hidden at .51 and inert at .60; it becomes actionable around .63. Small reversal across .4 repeats the editorial switch while the court itself continues to interpolate.

**Persist / respond.** Keep the court attached to the scroll playhead. Match the invitation to the point at which the controls work. Headline/copy movement is editorial and must not be mistaken for tennis information.

**Smallest intervention.** Delay the “open each group” invitation until its controls are actionable. Test a fixed headline anchor during the handoff before introducing any text transition. Preserve the court split and its immediate reversal; do not add scroll easing or a second animation clock.

**Verification.** Scrub .39–.64 in both directions, stop mid-transition and activate with keyboard. No instruction should refer to unavailable controls. Compare whether a reader follows the category split without looking away to chase the heading. The spatial jump and inactive interval are demonstrated; their effect on comprehension is a design judgment.

Code: [tactical paint logic](../../gui/margins-experiment/tactical-demo/demo.js), lines 86–111. Exact threshold samples are in `journey-check.json`.

### 4. Medium: the objection changes the answer without retaining its comparison

**Reader’s task.** Test whether return points explain the drop-shot disadvantage.

**Observed behavior.** The denominator change is meaningful: 110 points become 52 service points; drop-shot results change 3/11→1/5, while serve-and-volley remains 11/11. But the prior result is overwritten, 58 marks disappear and the remaining marks are repacked. The reader must remember the first fraction to explain the test. Repeatedly opening and closing results reveals the same facts; it is the denominator change that supports a real challenge.

**Persist / respond.** Keep the unchanged 11/11 as an anchor and make the changed drop-shot denominator legible. The reader controls inclusion, not an invented tennis chronology.

**Smallest intervention.** Add the before/after comparison to the existing scope note: removing return points changes drop-shot points from 3/11 to 1/5. No new control is needed. If more detail proves necessary, the removed drop-shot subset is exactly 2/6, derived from these records.

**Verification.** Toggle both ways and verify exact membership and all 110 source identities. Ask an uncoached reader what was removed and whether the objection eliminated the contrast. Success means an accurate explanation, not merely noticing that the fraction changed. The arithmetic is verified; the need for this annotation still requires an audience test.

Code: tactical `demo.js:31–77,118`; [independent source recomputation](../../reports/discovery/interaction-audit/source-fidelity.json).

## Motion to keep, reduce or reject

Keep the sculptural court split: it expresses an editorial decomposition and reverses with input. In the Wimbledon study, all 422 point nodes survive the forward/reversed chapter journey; set two stays an identifiable subset while the other four regroup. The reduced-motion path retains evidence inspection. This is a useful continuity reference within the existing project, not a proposal to combine the cases.

Preserve the bold neutral portraits and their fixed identities. The once-only 240 ms entrance/40 ms stagger is editorial. The existing 120 ms pointer hitter emphasis retargets under reversal, and keyboard input cancels it. Chrome’s Animation domain at quarter playback speed confirmed interruption during the active transition. System reduced motion removes movement; no additional portrait motion is needed. Its contribution to understanding has not been established by a reader study.

Reject ball flights, moving player positions, racket swings, reaction changes and replay timing: the records do not support them. Reject morphing a direction band across the court, which could imply a path between shots. Reject whole-panel crossfades, blur, shot-by-shot entrances, autoplay and a delayed next button: they obscure the record or reduce control. Reject animated counts and a decorative departure for 58 excluded marks. The prototype introduces **zero animation**; its native horizontal scroll is navigation through the record, with no duration encoding.

## Working comparison and iteration

Run from the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory gui/margins-experiment
```

- [Current interaction](http://127.0.0.1:8765/tactical-demo/#game)
- [Bounded prototype](http://127.0.0.1:8765/tactical-demo/?continuity=1#game)
- [Current recording, desktop](../../reports/discovery/interaction-audit/baseline/1440-journey.mp4)
- [Prototype recording, desktop](../../reports/discovery/interaction-audit/prototype/1440-journey.mp4)
- [Current recording, phone width](../../reports/discovery/interaction-audit/baseline/390-journey.mp4)
- [Prototype recording, phone width](../../reports/discovery/interaction-audit/prototype/390-journey.mp4)

Try point 150: inspect the first volley, go to the ending, then reverse to Medvedev’s intervening backhand. At 154, select specific earlier strokes. The records remain recognizable while the court shows only the current categorical fact. Recordings document scripted inspection pace, not historical shot timing or an uncoached reading.

The first prototype retained readable controls but introduced a long-record layout failure: 13 tiles expanded the desktop grid instead of scrolling inside it. The iteration constrains the existing figure/column and measures tile extents after layout using ResizeObserver. Shot input uses cached extents. Native scroll reveals only the selected tile; keyboard actions and reduced motion remain immediate. A first draft’s incorrect offset calculation was removed during this revision. Earlier captures/traces are retained as `prototype-v1/` and `performance-v1.json`; final evidence is `prototype/` and `performance.json`.

The remaining layout tradeoff is explicit: the readable record occupies more space above the court, and longer sequences require horizontal exploration. It does not keep every stroke or the entire explanation in one phone viewport. Test that cost with readers before making this the default.

## Verification and measured limits

The embedded 110 records agree field-for-field with `source-points.json` and their 215-point retained original specimen. Frozen subset SHA-256 remains `eb6f8cf0b7c3766f92f70424d9ec870a79a325e06360b4cba67b5444e62b1b5e`. The original charting workbook was inspected directly: directions describe crossing/projected crossing of the opponent’s baseline, not bounce positions. Only the documented completed return at 154/f39 receives a return-depth region. Later depth-like suffixes remain unmapped; 155 ends with the missed return and has no volley. The let preceding 154 is outside its 13 counted strokes. [Primary cell extracts](../../reports/discovery/interaction-audit/primary-definitions.json), [earlier full decode](2026-10-23-pressure-shot-evidence.md).

**676 checks passed** at 1440×900, 768×1024, 390×844, 320×568 and 1200×700. Checks cover all 20 active tokens/actors, ordered source fragments, stable controls, one selected/focusable stroke, active-tile visibility, page bounds, source-supported regions, no ball/player paths, native Arrow/Home/End/Tab input, boundary focus, rapid reversal and a live reduced-motion change. Chrome’s accessibility tree exposes player/stroke names. In emulated touch, a horizontal swipe moved the record 222 px while selected stroke and page scroll stayed fixed; tapping then selected the exact intended stroke. This is not a physical-phone or VoiceOver test.

Final performance comparison used 3 runs per version at each of 1440×900 and 390×844, in B/P/P/B/B/P order, with the same 24 native pointer actions plus four direct resets. Chrome DevTools timeline traces and Performance/Event Timing observers were recorded separately from video capture. These are warmed local interactions in installed Chrome on this Mac, without CPU/network throttling.

| Final local measurement | Current | Prototype |
| --- | ---: | ---: |
| Frame interval p95, desktop/phone runs | 16.7–16.8 ms | 16.7–16.8 ms |
| Observed intervals >25 ms | 0/509 | 0/499 |
| Observed long tasks >50 ms | 0 | 0 |
| Selector nodes removed per stress run | 364 | 0 |
| Median task duration, desktop | 147.49 ms | 108.03 ms |
| Median task duration, phone width | 114.51 ms | 119.31 ms |
| Layout events per run, desktop / phone | 30 / 30 | 46 / 54 |

The prototype removes selector churn but adds native scrolling work and more layout events. Desktop task duration fell in these samples; phone task duration rose slightly. Frame cadence was effectively unchanged. These samples establish that the prototype stayed within the observed frame budget; they do not prove a general performance improvement or a field INP result. Raw traces load in Chrome DevTools Performance. [Measurements](../../reports/discovery/interaction-audit/performance.json), [functional report](../../reports/discovery/interaction-audit/verification.json), [animation interruption](../../reports/discovery/interaction-audit/animation-check.json), [touch report](../../reports/discovery/interaction-audit/touch-check.json).

The design inspector’s generic findings were examined rather than treated as requirements to redesign: scoreboard names/skip link are not decorative eyebrows; the net texture, paper/italic identity and two portraits are inherited and pinned. Its demand for more pictures/video conflicts with this bounded evidence study. The size-count warning is a real maintenance observation, but reducing all typography is outside the selected interaction. No clean universal design score is claimed.

**Demonstrated:** source fidelity, readable addressable stroke records, persistent selector identity, keyboard/touch control, interruption behavior, reduced-motion behavior and measured local frame cadence. **Not demonstrated:** improved comprehension, expert surprise, voluntary exploration, reader preference, cross-browser behavior or physical-phone usability. No uncoached participant was available and none was simulated. A neutral later observation would ask a knowledgeable fan to explain the pressure sequence and challenge the choice of examples, without naming either volley or showing this audit first. Compare explanation accuracy, mistaken tracking/timing inferences and voluntary return to earlier evidence; observe scroll/focus losses. Do not claim audience improvement from automated checks.

## Scope and reproducibility

Implementation: the two `continuity-prototype` files, a conditional selector hook in `pressure-shots.js`, and script/style references in tactical `index.html`. `demo.js`, `demo.css`, `player-portraits.js`, source data, portrait assets and the Wimbledon implementation were preserved. Findings 2–4 remain proposed. There is no production integration or publishing.

Baseline source copies, scripts, screenshots, recordings, raw traces and results live under ignored `reports/discovery/interaction-audit/`. Reproduce with `capture.mjs baseline`, `capture.mjs prototype`, `verify.mjs`, `journey-check.mjs`, `measure.mjs`, `animation-check.mjs` and `touch-check.mjs` using Node 22+ and installed Chrome; the scripts use the already-installed local skill CDP helper and ffmpeg. Run performance measurement alone, with capture/inspection stopped. The initial browser MCP failed because its profile was already in use; an isolated disposable Chrome profile supplied DevTools evidence, and the native in-app browser supplied live reader interaction. Existing user browser profiles were untouched.

HEAD remains `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`, branch `experiment/margins-ledger`. Pre-existing untracked implementation and upstream CSV deletions were preserved. No paid usage, dependency installation, source CSV change, commit or remote write occurred.
