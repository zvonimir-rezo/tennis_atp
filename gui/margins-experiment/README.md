# Margins — The anatomy of almost

One authored Wimbledon 2019 investigation, expressed as a sculptural grass court over warm ivory. This disposable local experiment is not a production application or commitment to a publication schedule. The approved replacement world is recorded in [REDESIGN.md](REDESIGN.md); its current tokens and component rules are in [DESIGN.md](DESIGN.md) and [.impeccable/design.json](.impeccable/design.json).

Open `index.html` directly in a browser, or from the repository root run:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory gui/margins-experiment
```

Then open http://127.0.0.1:8765/. The page loads local records, fonts and turf material; no backend, framework, WebGL or package dependency is required.

## Experience and files

The continuous sequence is whole court → five categorical set sections → hold set two apart → opposing margins in the other four sets → bounded verdict. Scroll directly controls the composition: stopping holds it and reversing retraces it. All 422 native SVG point marks persist. Equal court sections name sets; their area does not encode point counts or shot locations. Exact record inspection is immediate.

`index.html` loads `records.js`, `court.js`, `evidence.js` and `style.css`. `court.js` builds the CSS 3D court and SVG point field, using event-driven requestAnimationFrame paints of the scroll playhead. Layout dimensions are measured on resize/preference changes; the scroll loop retains native SVG translate/scale objects and leaves stationary records untouched. `evidence.js` handles subsets, pre-point scores and exact record access. The old WAAPI controller in `app.js` is not loaded. `verify.html` is the older ledger bench; use `verify-court.html` for this replacement experience.

System or explicit reduced motion hides the 3D scene, collapses the long scroll section and supplies static evidence chapters through the navigation. The explicit control retains the current chapter (opening resolves to the verdict); when collapse happens inside the stage, the viewport returns to the opening stage to keep the composition visible. Returning to full motion restores the matching chapter stop. The system preference disables the explicit toggle. The records, objection and inspector remain available.

## Pinned evidence

`records.js` embeds the original-format 422-record subset without changing field values. Source match identity: `20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic`. Retained JSON SHA-256:

`b772afeb9e76baa3f0c7c21c0351ae72dddfcf47afe2111378b6bfeb720e89f3`

Original source: Jeff Sackmann's Match Charting Project, `charting-m-points-2010s.csv`; charted by Zindaras. [Original match report](https://www.tennisabstract.com/charting/20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic.html). Data license: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Preserve attribution and license for adaptations. This experiment is not a legal determination about a future portfolio publication.

Counts: 218/204 overall; set two 26/12; other four sets 192/192. The complete disjoint partition contains 38/33/351 records with winner counts 26:12, 12:21 and 180:171. Set two stays held while the other four split into −9 in tiebreaks and +9 elsewhere. Pre-point scores are normalized from server/returner to Federer/Djokovic order. The fifth-set breaker is at 12–12. There are no point timestamps, physical coordinates, modeled leverage or causal psychological claims.

The 192–192 finding was already published in 2019; the page credits it. The verdict concerns the limits of aggregate totals, not deservedness or counterfactual history. The [implementation review](../../docs/research/2026-10-21-margins-implementation-review.md) independently replays all 422 source records.

## Assets and capture provenance

Instrument Serif Regular and Italic come from the [official Google Fonts source](https://github.com/google/fonts/tree/main/ofl/instrumentserif); their OFL is retained in `assets/OFL-InstrumentSerif.txt`. Body text uses Arial/Helvetica. The retained Barlow asset belongs to the superseded ledger identity and is not loaded by the current page.

`assets/grass-turf.webp` is image-generated illustrative material, not a photograph of the 2019 court or match evidence. Its [provenance](assets/grass-turf-provenance.md) records the tool, original, encoding and generation prompt; the [image sidecar](assets/grass-turf.webp.json) retains the prompt and creation time. CSS and native SVG supply court geometry, chalk lines, net, depth, lighting and shadow.

Responsive targets refer to CSS viewport dimensions, not screenshot pixel dimensions or the turf raster. Captures should frame the rendered page and exclude browser chrome. Native capture dimensions and actual viewport measurements must be recorded separately; neither implies a physical-phone test.

## Verification and limits

Latest narrative refinement: set two arrives first, its +14 anchors the view, and the exact192–192comparison is available before the conclusion. No new controls or data. `debug/argument-transition.html` exposes a disposable playhead study and43targeted assertions. [Motion critique and verification](../../docs/research/2026-10-22-margins-argument-handoff.md).

Current 2026-10-22 ball/composition revision: **1275/1275 assertions** across60stable compositions, plus **8/8 scroll-work checks**. All422records and equal units persist. Live desktop1440×900 and phone390×844 profiling passed: callback p95 0.5/0.4ms, frame p95 18.6ms, no intervals above25ms in these single local runs. Physical phones remain untested. [Changes, review, exact method and artifacts](../../docs/research/2026-10-22-margins-ball-composition.md).

Open http://127.0.0.1:8765/verify-court.html and press **Run browser verification**. This separate bench exercises the actual page against `verification-oracle.js`, independently mapped from the frozen source. It checks record identities, exact group membership and scores, persistent marks, geometry, text clearance, keyboard inspection, reversal and reduced-motion behavior. It deliberately does not appear in the reader navigation.

Historical 2026-10-21 scroll performance revision: **754/754 assertions** passed in the in-app browser, covering40stable compositions plus source records, scores, interruption, inspection and reduced motion. The separate work regression passed **8/8 checks in IAB and Chrome155**, including zero synchronous scroll-loop layout reads, stable cue content, held-set continuity and every native SVG matrix at intermediate/reversed/resized positions. Tolerance is0.0001px; maximum observed error is0.00006095px. These two browser sessions share the Chromium engine. Original pre-performance reports remain historical evidence, not the current runtime certificate.

Open `debug/verify-scroll-work.html` for that regression, or `debug/scroll-profile.html` for live observer-free timing. The retained original renderer comparison applies to the historical performance revision; do not compare it under the newer ball/composition CSS as if it were an isolated renderer change. The artwork is present during timing. Write counters run separately; native translations are counted explicitly because they do not generate the same CSS attribute mutations. Do not run other browser tests during a profile.

| Actual viewport / session | Median of three p95 callback times, original → revised | Revised p95 frame interval |
| --- | --- | --- |
|1152×720 / Chrome155|4.2 →2.4ms|17.6ms|
|390×844 / IAB Chromium155|1.4 →0.4ms|17.5–17.6ms|

Desktop intervals above25ms fell from16/673(2.38%) to6/708(0.85%); phone-viewport runs had none before or after. Every revised run met the local cadence gate(p95≤20ms,≤5% intervals above25ms). The additional2ms callback headroom target passed1/3desktop runs and3/3phone runs. Rare desktop gaps up to99.7ms remain; their cause is not established by callback timers. These results do not certify perfect60fps, GPU/compositor behavior, physical phones, or other browser engines. [Diagnosis, method, raw artifacts and independent review](../../docs/research/2026-10-21-margins-scroll-performance.md).

The fresh visual review scored its material fixes resolved and returned ship at visual-review scope. A final short reduced-motion capture verifies normal-flow masthead/title separation; its footer is reachable by ordinary page scrolling. Expert-fan comprehension and appeal remain untested.

The [court visual review](../../docs/research/2026-10-21-margins-court-visual-review.md) retains the replacement direction. Its fresh finish pass judged the listed fixes resolved and returned a scoped ship verdict subject to the current browser checks completing. That verdict does not certify the whole experience or motion feel. Browser assertions and rAF diagnostics do not establish demand, artistic appeal, reader understanding, compositor performance or physical-phone performance. The planned uncoached five-fan observation and physical-phone testing have not occurred.
