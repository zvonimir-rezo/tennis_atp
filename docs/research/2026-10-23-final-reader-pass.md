# Final reader pass — 23 October 2026

Subsequent correction: the [UI overlap audit](2026-10-23-ui-overlap-repair.md) reproduced and fixed collisions outside this pass’s original viewport coverage. Its findings and expanded validation supersede layout-completion claims here; source and interaction evidence below remains the original checkpoint.

The existing tactical experience now uses the readable shot record by default and resolves all four priorities from the [interaction audit](2026-10-23-interaction-continuity-audit.md). The court split, bold neutral portraits and bounded argument remain. No case, feature collection, replay, reusable system or wholesale redesign was introduced.

[Open the completed experience](http://127.0.0.1:8765/tactical-demo/). No comparison query is needed. The former query resolves to the same final behavior. [Run instructions and controls](../../gui/margins-experiment/tactical-demo/README.md).

## What changed and why

| Priority / reader task | Previous failure | Completed intervention | Demonstrated verification |
| --- | --- | --- | --- |
| 1. Inspect how the pressure point unfolds | Numbered controls and replacing explanations made every stroke feel like another slide | Existing selector now retains readable player/stroke/exact-code tiles within a point. Selection and court facts respond immediately; native horizontal scroll only reveals the selected tile. No transition was added | All 20 tokens and actors match; 13/13 controls persist within point 154; zero selector removals per stress run, previously 364. Native arrows/Home/End/Tab, swipe/tap and rapid reversal pass |
| 2. Challenge the edit without losing place | Selecting a non-illustrated point removed the figure and displaced the controls by more than 800 px; moments restarted at serve | Existing complete-game controls precede a persistent inspection frame. Other points show the real result and exact original strings with an explicit unavailable-shot statement. Each prepared moment remembers its selected stroke | All 14 selections retain control position (0 px displacement at seven sizes), focus and source identity. Double faults 146/148 remain inspectable. Returning to 150/154/155 restores the stroke actually left |
| 3. Follow the split and act on its invitation | Heading jumped at progress .4 and copy invited clicks while controls remained inert | Editorial type follows the same reversible scroll playhead. Neutral handoff copy precedes the invitation, which appears only when controls become actionable. Pointer smooth scrolling can be interrupted; keyboard navigation is immediate | Samples on both sides of the former seam change by less than 3 px and reverse to the identical pose. No invitation references inert controls. Reduced-motion changes preserve the later article's viewport |
| 4. Explain the scope test | The first fraction disappeared when 58 return points were removed | Existing comparison area retains “3/11 overall → 1/5 on serve” and the unchanged 11/11 anchor after the test, including reversal | Both scopes, exact memberships, denominators and winners agree with all 110 original records. Comparison persists and focus moves to the available reversal control |

Final polish keeps those repairs usable on actual small surfaces: shorter reveal/action labels, non-overlapping equal point marks, 44 px full-game targets, readable stroke tiles, consistent score status height and visible keyboard focus. Native landscape and high zoom use the full static split in ordinary page flow rather than trapping the evidence in a short sticky viewport. Tablet and desktop keep the original composition; phones retain the portrait pairing before the inspection controls.

The main portrait WebPs are lossless and pixel-identical to the originals; original PNGs/provenance remain. Small hitter derivatives avoid decoding the full artwork again. This is a delivery optimization, not regenerated artwork.

## Motion decisions

Keep the scroll-driven court split as an editorial decomposition, not tennis motion. The title and copy share its playhead; stopping or reversing input stops or reverses the composition. No extra easing clock or font-size animation competes with it. Completed progress is cached, so scrolling the rest of the article does not repaint an unchanged split.

Keep the once-only 240 ms portrait entrance/40 ms stagger and interruptible 120 ms pointer hitter emphasis. Keyboard input cancels movement immediately; reduced motion uses only brief opacity feedback. Chrome's Animation domain at quarter speed confirmed active transitions retarget on reversal and settle immediately for keyboard input.

Reject whole-panel fades, shot-by-shot entrances, blur, autoplay, animated counts, decorative exits for excluded points and any delay before the next input. Reject flights, player positions, direction-band travel, racket swings, emotion changes or shot timing: none is supported by the records. The readable sequence adds no animation. Its value is persistent context and direct control.

## Evidence and iterations

The final pass corrected failures discovered during verification: a 1.5 px score-status height change, a 94 px viewport offset when changing motion preferences, and overlapping marks on the shortest phone. The independent standards review flagged the phone spacing; it was fixed and independently re-reviewed. Intermediate copy was shortened to avoid a legend collision during the handoff. Landscape/high-zoom inspection prompted the static, normally scrolling layout. A final visual pass removed repeated result text on non-illustrated points. Independent review caught the resulting hidden live-region issue; a persistent polite status now carries the exact selected-point outcome outside the hidden secondary summary. Chrome accessibility-tree checks confirm its semantics; actual spoken output remains untested. These changes were checked against the complete journey, not just a single selected shot.

The frozen 110 records still agree field-for-field with the original 215-point specimen. SHA-256 remains `eb6f8cf0b7c3766f92f70424d9ec870a79a325e06360b4cba67b5444e62b1b5e`. All 20 exact fragments/actors, service-box orientation, direction definitions and unsupported depth boundaries pass. Only completed return 154/f39 has return-depth shading; later suffixes remain unmapped. Point 154's let stays outside the counted 13 strokes; point 155 ends on the missed return without a volley. [Primary charting definitions](../../reports/discovery/interaction-audit/primary-definitions.json), [source decode](2026-10-23-pressure-shot-evidence.md).

**34,986 assertions pass** at 1440×900, 768×1024, 390×844, 320×568, 1200×700, 844×390 and 640×450. Coverage includes every source identity, all point-mark bounds and non-overlap, exact scope results, all 14 game records, stable selection/focus, all prepared strokes, supported court regions, absence of paths, native keyboard boundaries, restored moments, scroll reversal and live reduced motion. The 640×450 surface exercises the available width/height at 200% of a 1280×900 viewport; browser text enlargement and physical-device testing remain separate.

Chrome accessibility-tree inspection verifies meaningful stroke names and selection semantics. Emulated touch moved the native rail 212 px without changing the selected shot or page position, then tapped the exact intended stroke. No-JavaScript fallback exposes the bounded conclusion and record download. Native in-app-browser use exercised results, scope reversal, moment selection, keyboard stroke reversal, full-game disclosure and double-fault inspection. These are designer/tool checks, not an assistive-technology reading study.

Independent read-only specification and standards reviews inspected the final source against the request and before snapshots. Specification review found no outstanding mismatch. Standards review confirmed the mark-spacing correction and found no remaining actionable issue in the reviewed changes. The final static-height/progress-cache changes also received a standards followup with no actionable regression and passed the expanded seven-size regression.

## Measured browser performance

Twelve warmed runs: three per scenario (shot stress / scroll split) per viewport (1440×900 / 390×844), in installed Chrome on this Mac. DevTools timeline traces, Performance metrics, rAF intervals, long-task and layout-shift observers were collected separately from recording. The shot workload used 24 native pointer actions plus four direct resets, matching the prior audit workload. No CPU/network throttling or field INP claim.

| Measurement | Finished experience |
| --- | ---: |
| Frame interval p95, all 12 runs | 16.7–16.8 ms |
| Observed frame intervals >25 ms | 0 / 1,465 |
| Long tasks >50 ms | 0 |
| Selector nodes removed during same-point stress | 0 |
| Median shot-workload task time, desktop / phone | 118.41 / 106.98 ms |
| Median scroll-workload task time, desktop / phone | 98.48 / 100.42 ms |
| Layout events per shot run, desktop / phone | 46 / 54 |
| Layout shifts without recent input | 0 |

Input-associated shift entries were small (aggregate approximately .00030 desktop / .00108 phone per shot run); they are retained in the raw report, not called a universal zero-shift result. The original audit baseline recorded the same 16.7–16.8 ms cadence and zero long tasks. Removing selector churn is demonstrated; general speed or comprehension improvement is not. The main proven repair is control continuity: full-game controls now move 0 px rather than leaving the viewport.

[Raw measurements](../../reports/discovery/final-pass/performance.json) and `shot-*-trace.json` / `scroll-*-trace.json` in the same directory load in Chrome DevTools Performance. [Functional checks](../../reports/discovery/final-pass/verification.json), [animation/touch/fallback checks](../../reports/discovery/final-pass/edge-check.json), [portrait pixel comparison](../../reports/discovery/final-pass/portrait-pixel-check.json), [direct-file/explicit-motion/status smoke check](../../reports/discovery/final-pass/smoke.json).

## Working demonstration

- [Finished desktop journey](../../reports/discovery/final-pass/1440-journey.mp4) / [phone-width journey](../../reports/discovery/final-pass/390-journey.mp4).
- [Original desktop behavior](../../reports/discovery/interaction-audit/baseline/1440-journey.mp4) / [original phone behavior](../../reports/discovery/interaction-audit/baseline/390-journey.mp4).
- [Finished portrait/inspection composition](../../reports/discovery/final-pass/1440-game.png), [phone shot ending](../../reports/discovery/final-pass/390-ending.png), [short-phone comparison](../../reports/discovery/final-pass/320-split.png).

Recording pace is scripted and editorial; it is not shot timing. To inspect the repair: select point 150's first volley, jump to its ending, reverse to the intervening backhand, inspect a double fault in the complete game, then return to set point. The sequence, real source identity and inspection controls remain available.

## Limits and completion

The existing product is complete at the requested local scope. All four audit issues are implemented as default behavior; there is no remaining experimental toggle or required implementation decision. The former prototype files were removed from the served app; their before copies and historical recordings remain under ignored reports. No dependency, paid service, upstream CSV change, publishing or unrelated-project change was made.

No uncoached participant was available, and none was simulated. Better comprehension, voluntary exploration and appeal remain judgments for audience observation. Physical phones and a real screen-reader reading session remain unverified. Firefox automation failed because the installed driver and browser protocols do not match; WebKit remains unverified. No install/download was introduced, and the verified Firefox recovery attempt was not repeatedly retried. Chrome and native in-app-browser results do not stand in for those engines.

Evidence lives under ignored `reports/discovery/final-pass/`. Reproduce with `verify.mjs`, `edge-check.mjs`, `look.mjs`, `measure.mjs` and `capture.mjs` using the existing local CDP helper, installed Chrome and ffmpeg. Run measurements alone. Before-source copies are in `before/`. Current HEAD remains `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`, branch `experiment/margins-ledger`; no commit was requested.
