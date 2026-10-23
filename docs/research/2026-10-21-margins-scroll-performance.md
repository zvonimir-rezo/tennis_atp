# Margins scroll performance — 2026-10-21

Scope: optimize the approved sculptural court experiment without changing its artwork, argument, record identities or scroll rhythm. No dependencies, data/model changes, publication or feature additions.

## Diagnosis

The actual visible browser specimen is exercised through `gui/margins-experiment/debug/scroll-profile.html`. The source is fetched and executed unchanged except for identical `performance.now()` markers around the real `paint()` callback; the frozen original is `.impeccable/performance/baseline-court.js` (SHA-256 `8ed929ecd3661f75b2611e107656349881660677b1b00bb37062700b3d70c1a2`). Each sample warms a round trip for 1.2 s, measures forward/reverse scrolling for 4 s, then counts writes in a separate 2.2 s sweep. The timed pass has no MutationObserver, screenshots, polling or per-frame geometry reads from the harness. Three paired runs alternate baseline/live/live/baseline/baseline/live. Tests run sequentially, without other browser verification workloads.

A tight regression on the actual page, `debug/verify-scroll-work.html`, reproduced 295 synchronous layout reads and 59 replacements of unchanged cue content during a bounded cancellation/reverse. It also detected tiny writes to set two, whose intended held coordinates should remain fixed. All 422nodes already survived; identity loss was not the issue.

Ranked probes tested: redundant DOM/style work; point CSS transforms; artwork rendering; synchronous geometry reads. Original-source instrumentation localized the largest callback segment to point updates. Freezing those writes reduced callback p95 from 5.1 ms to 2.8 ms; keeping cue content stable gave 3.2 ms; caching geometry reads gave 2.7 ms. Hiding the textured court did not help (4.1ms). These individual diagnostic runs varied and are not additive causal estimates or final performance comparisons. Their useful finding was to keep the artwork and optimize the rendering loop. A native SVG translation probe justified testing that narrower seam.

The bottleneck addressed is repeated scroll-callback DOM/style work: layout reads after narrative writes, per-frame content replacement, allocation/recalculation of stationary point geometry and 422 CSS-transform string updates while points travel. The fix caches dimensions on resize/preference changes, keeps stable nodes/content, updates positions only when needed and uses retained native SVG translation/scale objects on the same 422elements. Set two explicitly uses its held coordinates rather than floating-point cancellation. No smoothing tail, new timeline, canvas replacement, texture reduction or missing record is introduced. A bounded pitch adjustment protects the smallest 320 px layout when a classic scrollbar narrows the actual drawing surface; already-fitting layouts keep their existing pitch and every symbol retains its area.

## Evidence and limits

The final measurements and verification results follow. Raw JSON/text and captures live under `gui/margins-experiment/.impeccable/review/perf-*`.

This is a callback profile plus controlled rendering-path isolation, not a Chrome CPU/GPU trace. The DevTools connector could not attach because its profile was already in use; native-app access was unavailable. Browser Long Animation Frame observation did not yield useful attribution in the iframe and is not used as evidence of no jank. The API's reporting threshold is 50 ms, so it would not diagnose every missed 60 Hz frame anyway ([Chrome documentation](https://developer.chrome.com/docs/web-platform/long-animation-frames)).

Native SVG transform wrapper identity is unreliable in the tested Chromium path. Tests compare actual matrix values, not wrapper object equality; the profile counts all native `setTranslate` calls separately from CSS attribute mutations. Fewer MutationObserver records alone would not establish fewer record movements ([SVGWG discussion](https://lists.w3.org/Archives/Public/public-svg-issues/2026Sep/0092.html)).

Frame cadence gate: p95 interval≤20ms and≤5% intervals above25ms in this local60Hz environment. Callback≤2ms is an additional headroom target, not a physical-device certificate. Runtime can include host scheduling pauses; maximum intervals remain visible in raw results rather than being trimmed. No physical iOS/Android device, Safari/Firefox certification or reader-comprehension test occurred.

## Final results

| Actual browser viewport / session | Original p95 callback(ms), three runs | Revised p95 callback(ms), three runs | Median improvement |
| --- | --- | --- | --- |
|1152×720 Chrome155|5.4 /4.0 /4.2|2.4 /1.6 /2.4|43%|
|390×844 IAB Chromium155|1.2 /1.5 /1.4|0.4 /0.4 /0.3|71%|

The desktop browser's actual client width was 1140 px; the phone viewport's actual client width was 375 px, due to classic scrollbars. Nominal requested dimensions are not substituted for observed dimensions. Both paths use Chrome 155, not two engines. The measured source hash was `4a6d008a03d496a2b026bfdf38ffba419b5fbbeb94b12b29131dbeb2c6af8890`.

All revised runs met the frame-cadence gate. Desktop p95 intervals were 17.6 ms; intervals above25ms fell from 16/673(2.38%) to 6/708(0.85%). Rare long gaps remained, up to 99.7 ms in the revised runs, and are not attributed conclusively. The2ms callback headroom target passed 1/3desktop runs and 3/3phone runs. Phone p95 intervals were 17.5–17.6ms with no intervals above25ms. The phone baseline was already meeting cadence; the new result is added callback headroom, not proof of a previously broken phone frame rate.

The separate phone write-count sweep retained 16,120 native point translations while eliminating per-point CSS style writes. This preserves the underlying motion rather than omitting records. Its other attribute mutations fell from 17,467 to 1,021; unchanged cue replacements fell from 132 to0. The desktop count fields from the first paired artifact used an SVG wrapper-identity comparison and therefore misreported native translations as 0; those particular counters are invalid and are not used. Timing in that artifact is still valid because counters ran separately. The harness now counts all actual native setTranslate calls and rejects empty/insufficient timing samples; single/paired verdict summaries use the same aggregate result.

Verification:

- **754/754 actual-browser invariants passed**, including 40stable desktop/phone/short compositions, independent source totals/subsets/scores, all422identities, mark bounds/text clearance, keyboard inspection, rapid interruption/reversal and reduced motion.
- **8/8 work/matrix checks passed in IAB and separate Chrome155.** The bounded cancellation/reverse now performs 0synchronous layout reads, 0cue replacements and 0held-point translation calls. All 422nodes remain the same objects. Actual native SVG matrices match every record at 15forward/reverse fractions across 1440×900,390×844and320×590. Maximum matrix error 0.00006095 px, under the 0.0001 px tolerance.
- Actual wheel scroll and reversal were replayed on desktop and phone layouts. Clicking moved point 360 in both opened its exact 40–30,2–2sets,8–7games,Federer-serve,Djokovic-win record. Native keyboard Right advanced to point 361 (40–40). Static reduced mode retained 422records and hid the 3D scene.
- CSS, turf material, fonts, records and evidence module hashes match the pre-performance artifact. Independent source review approved native transform order, cache invalidation, held coordinates and the bounded narrow-phone adjustment. It also caught profiler-summary weaknesses; those are corrected. This is scoped code/verification review, not an independent fan or physical-device study.

Artifacts: `gui/margins-experiment/.impeccable/review/perf-paired-chrome-desktop.json`, `perf-paired-iab-phone.json`, `perf-invariants-final-iab.txt`, `perf-work-final-chrome.json`, `perf-work-final-iab.json`; intermediate diagnostic probes are prefixed `perf-probe-`. Native screenshots include `perf-desktop-preserved.png`, `perf-desktop-scroll-cut.png`, `perf-phone-preserved.png`, `perf-phone-scroll-cut.png` and `perf-phone-evidence.png`. These are page captures; actual CSS viewport values are stated separately. The final file hashes are in `reports/discovery/margins-scroll-artifact-manifest.json`.

The improvement is a smaller, more stable scroll callback with preserved artwork and independently checked record continuity. Full physical-device or compositor certification remains outside the available evidence.
