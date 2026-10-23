# UI overlap audit and repair — 23 October 2026

The reported overlaps were reproducible. The prior seven-size functional checks missed short desktop windows, wide phones and intersections during scrolling. This pass repairs the existing layout without changing the portraits, source records, pressure sequences or scope.

[Live page](http://127.0.0.1:8765/tactical-demo/). Changed application files: `demo.css` and `demo.js` only.

## Findings and completed repairs

| Priority | Reproduced failure | Cause and repair |
| --- | --- | --- |
| P1 | At 761×600 all 110 marks escaped their result panels and reached the footer. At 900×700, 274 pairs of marks overlapped after opening results | Fixed plot/header offsets left too little room and allowed negative or sub-diameter spacing. The renderer now measures the actual visible headers after wrapping/disclosure. Constrained panels use equal smaller marks and suitable columns. Short windows use the existing complete static split in normal document flow, with enough stage height |
| P1 | At 760×740 the opening court sat behind the copy, start button and footer; native phone-width inspection also showed footer text over the court | The opening object's size/position ignored the space left by the text. Its existing slab/net geometry now fits a clear area between the opening action and footer on phones, and alongside the text on desktop. Uniform three-dimensional scaling keeps the projection proportional. Headline size also responds to height |
| P2 | Copy crossed the court during the scroll handoff. At 1366×768 the start button overlapped “The whole second set” | The diagonal copy path crossed the artwork, and the supporting note was independently bottom-anchored. Copy now leaves before its position changes and returns above the split, all driven reversibly by the same scroll progress. The optional supporting note hides when it would collide with the action. The main heading, court and controls remain |
| P3 | “The cut. And its limits.” wrapped onto three lines on the narrowest phone | The mobile source heading now fits its intended two-line measure. Heading leading has enough room for the actual typeface |

The static threshold is now 560 CSS pixels of height, or 650 pixels on widths above 760 pixels. This is a reading fallback for constrained windows; larger windows retain the reversible sculptural split. The opening geometry is recalculated after local fonts finish loading so cached fallback-font wrapping cannot leave stale positions.

No ball/player geometry, shot token, point membership, result, score, portrait pixel or source definition changed. The opening fit and copy handoff are editorial composition, not tennis information. No dependency or new feature was added.

## Verification

The expanded overlap probe checks **26 viewports and 494 states**: opening; eight intermediate/completed scroll positions; closed/open results; service scope; pressure introduction; complete game; shot ending; expanded court-method and raw-record disclosures; sources and their expanded record selector. Sizes include both sides of the 760/761 and 1050/1051 width boundaries, heights around the fallback boundary, 320-pixel phones, landscape and 1920×1080.

No collisions were detected in the final matrix: text ink bounds, court/text intersections during the opening, horizontal page overflow, point bounds or point-to-point intersections. Native closed-disclosure content is excluded from visible collision checks. Text checks use font ink metrics rather than oversized font boxes, and findings were compared with screenshots; this is not a claim of pixel-perfect coverage of every browser/device.

The original **34,986 source/interaction assertions pass** against the repairs. They cover all 110 original records, all 20 shot tokens/actors, exact group arithmetic, every point in the 14-point game, persistent controls, keyboard focus, moment restoration, reversal and live reduced motion. The frozen source SHA-256 remains `eb6f8cf0b7c3766f92f70424d9ec870a79a325e06360b4cba67b5444e62b1b5e`.

Quarter-speed Chrome animation checks confirm pointer reversal and immediate keyboard interruption. Synthesized touch scrolls the shot record without changing page position or selected stroke, then selects the intended tile. Direct-file loading, local fonts/assets, explicit motion changes, the polite result status and the no-JavaScript source fallback pass.

The final design inspector has no failures with three documented content exceptions: factual scoreboard/skip labels, the existing geometric court net and the bounded two-player imagery. Raw warnings remain: the inherited paper/italic identity, typography-size variety, literal source-code font, intentional horizontal shot navigation, absence of footage and a generic first-screen title heuristic. These are not suppressed as overlap fixes. All seven inspector images and the reproduced failure views were inspected. Cold-cache font checks confirm the font-ready pose agrees with an explicit fresh resize at all seven final screenshot sizes. [Final views and font checks](../../reports/discovery/ui-overlap-audit/finish.json). No generic “perfect UI” or WCAG certification is claimed.

Independent specification and standards reviews found no remaining actionable issue in the repairs, including the final copy handoff, font refresh and fallback behavior.

## Evidence

Local executable checks and before sources are under ignored `reports/discovery/ui-overlap-audit/`:

- [Original wide-phone collision](../../reports/discovery/ui-overlap-audit/before/760x740-opening.png) and [original short-desktop spill](../../reports/discovery/ui-overlap-audit/before/761x600-split-open.png).
- [Expanded overlap results](../../reports/discovery/ui-overlap-audit/validated/audit.json), [source/control regression](../../reports/discovery/ui-overlap-audit/verification.json), [touch/interruption/fallback checks](../../reports/discovery/ui-overlap-audit/edge-check.json), [direct-file/status checks](../../reports/discovery/ui-overlap-audit/smoke.json).
- [Final inspector output](../../reports/discovery/ui-overlap-audit/inspector-after-result.json), with screenshots in `inspector-after/`.

Eighteen final performance runs (three per workload/viewport: shot inspection, scroll split and result/scope changes at desktop and phone widths) recorded frame-interval p95 of 16.7–16.8 ms, no long tasks and no observed intervals over25ms across 1975 samples. Browser performance is measured separately from screenshots and functional checks; raw traces and the final measurements are saved in [performance.json](../../reports/discovery/ui-overlap-audit/performance.json). This is warmed local Chrome behavior, not a field INP measurement or physical-phone benchmark.

Audience, real screen-reader speech and physical-device usability remain untested. Firefox/WebKit coverage is unchanged from the previous pass. The current work corrects demonstrated collisions in the existing product; it does not claim to resolve those validation limits.
