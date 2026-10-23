# Margins disposable experiment — verification

2026-10-21. User authorized implementation of the bounded sequence after design planning. Local artifact: [index.html](../../gui/margins-experiment/index.html). Branch `experiment/margins-ledger`, base commit `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`. No production integration, publishing, participant recruitment, models, upstream CSV edits or package dependencies.

## Delivered experience

One authored sequence: full 422-point total → five set contributions → hold set two's 38 points apart → strongest objection and complete 38/33/351 partition → bounded verdict. All 422 keyed SVG point elements persist. Names, winner shapes/colors, denominator and record identities remain stable. Native WAAPI provides800/880 ms deliberate motion, shared-time pause, reverse and cancellation; repeated inspection is immediate. Source records, normalized pre-point scores, subsets and championship points359/360 are inspectable.

Actual design: Barlow Condensed ExtraBold, ink/paper/acid, equal-area Federer circles and Djokovic squares. Body uses local Arial/Helvetica rather than adding another font asset. Original Barlow font and OFL license retained. The phone composition is headline/deck → ledger → explanation → advance; DOM order matches that reading order. Advance returns focus to the new heading. Motion controls sit above the chart.

The visual review prompted a deliberate refinement to the planning spec: during travel, departure annotations move into a protected, fixed reference panel above the plot. The moving38-point bracket stays in the plot; its ID caption stays in the protected panel. This avoids points obscuring source labels when paused. The full-match422/218–204 summary stays visible. At rest, the source panel gives way to the large winner totals and the destination's full annotations.

## Evidence and source review

`records.js` was independently compared with the retained original-format JSON: every field in all 422 records agrees. Retained source SHA-256 remains `b772afeb9e76baa3f0c7c21c0351ae72dddfcf47afe2111378b6bfeb720e89f3`. Independent reviewer replayed all 422 pre-point sets, games, point scores, servers and game numbers. Counts and disjoint subsets agree with the [evidence audit](2026-10-21-motion-evidence-audit.md).

The [implementation review](2026-10-21-margins-implementation-review.md) found and then verified correction of source-annotation continuity, hidden focusable group controls and focus loss on settlement/resize. Final source disposition: no remaining material evidence, focus or controller blocker. This is source review, not proof of perceived continuity or appeal.

## Executable browser coverage

Open [verify.html](../../gui/margins-experiment/verify.html) and press **Run browser verification**. It exercises the actual page in an iframe against a separately generated Python record oracle. Final result: **255 checks passed**. Full run output: ignored `reports/discovery/margins-experiment/browser-checks.txt`.

Coverage:

- All 422 unique IDs and original winners at settled and intermediate states; finite coordinates; no deleted point elements; complete disjoint unions.
- Exact membership of set two, tiebreak and remaining-point selections; selected mark counts and restoration.
- Pre-point score/server fixtures76,81,87,88,125,188,198,359,360,413,422.
- Pause and reverse after 80/400/700 ms; five rapid chapter-retarget sequences; latest target wins; no leftover animations.
- Mid-motion inspection settles the exact destination; source labels protected outside moving plot.
- Group-focus preservation, focus transfer into the inspector, keyboard point stepping, Escape, and focused-Pause recovery during resize.
- Reduced-motion path using the explicit control; all records and meanings retained. System preference handling was reviewed in source, not independently emulated through the blocked DevTools plugin.
- All five chapters at 1440,768,390,360,320px iframe widths: no horizontal document overflow, marks inside stage, headline within its column and no endpoint point/count-label intersections. Phone DOM order and selected record survive breakpoint changes.

Separate firsthand CUA operation inspected1440×900 desktop and 390×844 phone compositions, every authored chapter, paused transfer, source/objection views and real keyboard Enter, ArrowRight359→360 and Escape→point input. Initial 1280×720 inspection exposed the below-fold opening action, corrected during development. Temporary viewport overrides were reset. Native phone focus outline measured `rgb(200,244,74)`.

Measured solid-color contrast on ink: paper 16.66:1, acid 14.59:1, secondary text 8.98:1, body text 11.27:1. Unselected point opacity was raised to .42; composited paper/djokovic context contrast is 3.81/3.45:1. Actual browser confirmed 33 selected tiebreak marks out of 422 and .42 context opacity.

## Runtime limits

The last recorded timing diagnostic observed 809 ms and 49 rAF intervals, with p95 17.9 ms and maximum 18.5 ms. This is a browser timing diagnostic, **not a compositor trace, physical-phone result or certified 16.7 ms p95 budget pass**. The bench's timing check confirms observations were collected; it is not a performance gate. No claim about LCP, CLS, throttled performance or physical-device smoothness is justified yet.

The DevTools plugin repeatedly reported a profile held by another browser session. That session was left intact; verification used the working in-app browser. No additional browser library, package or service was installed.

## Separate visual critique

The [visual review](2026-10-21-margins-visual-review.md) inspected actual desktop/phone endpoints and the paused intermediate. Its initial material fixes were protected annotation space, themed heading focus and consistent SVG arrows. Recaptures scored all three **resolved**, with no material regression visible. Its final **ship** disposition covers those scored fixes for this disposable experiment; it does not certify the whole surface, motion feel or audience appeal.

Screenshots are retained under ignored `reports/discovery/margins-experiment/`: desktop opening, sets, intermediate, concentration, objection, verdict; phone opening, concentration, intermediate, objection. Measured count/overflow/contrast/focus defects are distinct from the reviewer's judgments about sporting force, hierarchy and coherence. Impeccable detector ran once. Its 11px record-position warning was corrected to 14px; its Arial warning is an intentional supporting-text choice, and its source-section flush-padding warning is inconsistent with the rendered percentage insets. No claim of an unqualified detector pass.

## Still untested

No five-fan observation, physical-phone session, cross-engine matrix, 200% browser-zoom pass or live system reduced-motion emulation has occurred. The [planned observation criteria](2026-10-21-margins-design-motion-spec.md) remain:4/5 operate unaided;3/5 substantiate new/sharpened understanding versus their prior account;3/5 voluntarily inspect;4/5 understand the verdict's limits. Numerical novelty, compliments and completion are insufficient. Do not recruit or contact participants without authorization.

Run instructions and provenance are in the artifact's [README](../../gui/margins-experiment/README.md). The local experiment opens without a backend; the optional standard-library HTTP server only serves its static files. Unrelated working-tree changes were preserved. No production promotion or ongoing maintenance commitment follows from this build.

## Focused critique revision

Superseding browser run:273/273 assertions passed after the objection was revised around cancellation, preserving set two as a fixed anchor. Added checks cover exactly384 animated records, fixed38 coordinates and annotation, pause/reverse, immediate unchanged verdict, phone focal landing and viewport anchor delta0. A targeted geometry trace diagnosed and verified the embedded-engine scroll-preservation fix. Final diagnostic:821ms,49rAFintervals,p95 17.6ms,max17.7ms. This remains a timing diagnostic, not compositor certification or physical-phone measurement.

Desktop/phone source and visual reviews found no remaining blocker in this focused change. Human comprehension and voluntary exploration remain untested. See2026-10-21-margins-focused-critique.md and ignoredcritique-after-* captures. Frozen records and source hash unchanged.
