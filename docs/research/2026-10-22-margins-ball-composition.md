# Margins: evidence composition and tennis-ball units

Delivered 2026-10-22 on `experiment/margins-ledger`, HEAD `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`. Local, uncommitted experiment; no dependency, source-data, modeling or publishing changes. Unrelated changes preserved.

## What changed

The supplied wide verdict mixed giant type, a legend and loosely positioned textured slabs. Separate narrative, legend, evidence and footer bands now prevent collisions. Group labels, record lanes and slab bounds share one layout; top-left slab origins remove centre-scaling drift. Five initial set fragments retain equal dimensions. Later analytical surfaces fit their contents, with a structural green edge and restrained pale ground; the opening turf, court geometry, net, depth and shadow remain. The floor shadow fades as the object becomes a diagram, and the camera is flat by the five-set stop.

Each persistent record is an equal-radius SVG ball disc with one seam path. Federer stays green, Djokovic plum; explicit names and F/D lanes carry identity. Djokovic’s seam is rotated, but tiny seam orientation is not required for identification. Desktop balls are larger than phone balls; the unit area is equal within every viewport. No per-ball shadows, filters, textures, gradients or animation loops. All 422 native transform groups persist.

The default point-1 ring is gone. Only intentional point selection creates a halo. Real ball clicks retain exact source identity and open inspection. Samples remain fractions of 422; five-set labels use compact fractions with the nearby unit legend. The big 192–192 comparison remains distinct from the signed margins.

Short-phone review exposed overlapping surfaces even while records cleared text. A new assertion checks physical deck separation too. A first attempted smaller tiebreak header failed text-ink checks and was rejected. The delivered layout preserves its original 100px header, gives the short-phone evidence field 12px more height, and derives the lower surface’s position from the actual upper surface plus at least 8px. Set two stays fixed through the split.

## Executable evidence

- `verify-court.html`: **1275/1275 assertions passed**, including 60 stable compositions, frozen independent oracle identity/membership/totals/pre-point scores, equal ball units, all record bounds, mark separation, actual text-ink clearance, narrative/legend clearance, slab alignment and separation, resizing, reversal, interruption, keyboard and reduced motion.
- Dimensions include 1909×872 (supplied screenshot condition), 1440×900, 1440×720, 1024×650, 768×900/650, 390×900/844, 320×900/650/590 and 404×590. These are CSS viewports, not physical devices.
- `debug/verify-scroll-work.html`: **8/8 checks passed**. No synchronous layout reads or cue replacement during scroll; no held-set point translation writes during cancellation; 422 persistent record groups. Every native matrix matches source geometry across 45 intermediate/reverse/resize samples; maximum error 0.00006027px, tolerance 0.0001px.
- Real pointer clicks on a ball opened point 360 on desktop and phone: Federer serving at 40–30, completed sets 2–2 and games 8–7, Djokovic won the point. Keyboard Right in focused record details moved to 361, 40–40.
- Actual wheel forward/reverse and static reduced-motion path checked. JS syntax checks passed.

Records remain unchanged: `records.js` SHA-256 `78c101d6f1114435b040c2849c5f0c2f35b9ca112458627259fe5273acbd3e5a`. The published 192–192 finding remains attributed; no new research claim or causal interpretation was introduced.

## Runtime: final revision only

Observer-free 4-second forward/reverse samples after a 1.2-second warm-up; counters run in a separate sweep, with no concurrent verification workload. IAB Chromium 155 on this Mac. Each row is one local run, not a population estimate or a before/after improvement claim.

| CSS viewport | Frame samples | p95 interval | Intervals >25ms | p95 callback | Max callback |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1440×900 | 241 | 18.6ms | 0 | 0.5ms | 1.4ms |
| 390×844 | 241 | 18.6ms | 0 | 0.4ms | 1.2ms |

Both passed the local cadence gate (p95≤20ms and ≤5% above25ms) and callback headroom gate (p95≤2ms). These are browser callback and rAF measurements with artwork present, not a GPU/compositor trace or a guarantee of perfect60fps. Physical phones and other browser engines remain untested. The older paired performance report is historical; its original renderer should not be compared under the new CSS as an isolated change.

## Visual critique and limits

Independent final source/render review found no blockers in wide verdict, wide even-total reveal, tall-phone objection, short five-set and short objection captures. The review judged the larger desktop symbols readable as tennis pictograms, the upper editorial hierarchy deliberate, and the stacked phone comparison coherent. This is aesthetic judgment grounded in rendered composition, not measured audience appeal. Expanded bounds and ink assertions supply separate executable evidence.

Impeccable’s detector was run once. Its visible warnings included cream ground, italic serif, Arial, container padding and design metadata ramps. The approved sports-editorial world deliberately retains ivory, Instrument Serif and a plain supporting face. Existing closing sections have actual responsive padding; no broad restyling was undertaken to satisfy generic heuristics. PRODUCT legacy schema and the DESIGN sidecar remain stale; those metadata repairs were left outside this UI task. A later short-phone spacing correction was verified manually and by the expanded browser bench.

Five knowledgeable fans have not been observed; comprehension, surprising insight and voluntary continued inspection are still unproven. No demand, novelty or physical-phone performance claim follows from this work.

## Artifacts

Before source: `gui/margins-experiment/.impeccable/balls-before/`.

Final captures and raw reports: `gui/margins-experiment/.impeccable/review/balls-*`, specifically `balls-wide-verdict.png`, `balls-wide-even.png`, `balls-phone-objection.png`, `balls-short-five.png`, `balls-short-objection.png`, `balls-final-verification.txt`, `balls-final-scroll-work.json`, `balls-runtime-desktop.json`, and `balls-runtime-phone.json`. Early first/second verification reports are superseded. Captures are page-only; actual CSS viewports are stated above.
