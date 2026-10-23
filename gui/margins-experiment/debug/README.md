# Scroll diagnostics

Serve the experiment as described in the parent README. These pages are debug tools outside the reader navigation.

- `/debug/verify-scroll-work.html`: press **Verify scroll work**. Exercises the real renderer, layout-read/cue/held-point contracts, all422node identities, and actual native matrices at intermediate, reversed and resized positions. Matrix tolerance is0.0001px. It deliberately patches measurement APIs only in its test iframe and restores them afterward.
- `/debug/scroll-profile.html`: press **Compare three paired runs**. Runs baseline/live/live/baseline/baseline/live sequentially, with visible artwork, warmed caches, observer-free4s timing and a separate2.2s write-count sweep. The frozen original is `../.impeccable/performance/baseline-court.js`; the live renderer is fetched fresh. Source hashes and actual viewport/client widths are included. Do not run other tests or capture screenshots during timing.

The cadence gate is p95≤20ms and≤5% intervals above25ms, with adequate samples. The additional callback headroom target is p95≤2ms. Both have separate fields in the result; overall pass requires both. Count native translation calls separately from CSS attribute mutations. A browser viewport is not a physical device, callback timing is not a GPU trace, and a passed budget is not a perfect60fps certificate.

Full independent source/record/layout assertions remain in `/verify-court.html`. The performance diagnosis and limitations are in `docs/research/2026-10-21-margins-scroll-performance.md` from the repository root.
