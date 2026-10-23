# One focus at a time — 2026-10-23

Superseded: the user rejected this design. The preceding experience was restored and polished; see 2026-10-23-restore-polish-release.md. This report records the rejected version only.

Status: implemented, verified and independently reviewed after the user rejected the previous simplification as still busy. Branch codex/fan-evidence-journey; HEAD 2c40e40c0f3ac51cc11eabe6c7c25932234e83e0. Preserve unrelated untracked application/deletions. Baseline source copies under ignored reports/discovery/focus-journey/before/.

Diagnosis: hiding codes did not fix simultaneous tasks. Default page still presents a three-group reveal, serving filter, complete ledger, moment tabs, two scoreboards/portrait systems, shot controls/court and technical caveats. More presentation polish will not resolve this. Explicit user direction now permits replacing that main path.

Bounded change: replace the scroll-controlled multi-panel main path with one initial comparison, then one selected pressure moment at a time and a short conclusion. Exact cohort ledger, shot diagram, all 14 game records and methodology open only on request. Keep existing frozen data, exact shot decoder, native details, source download, serif/ivory/player colours, score orientation and historical limitations. Remove redundant introductory action, mandatory long court scroll, default ledger, moment tabs and duplicate portraits from the main path. Do not add a case, model, dependency or generated asset.

Hypothesis: a reader can follow comparison → selected moment → point outcome → next moment without choosing among competing inspectors. This is a structural hypothesis, not an asserted learning improvement.

Acceptance fixed before editing:
- Default main view has one primary action; only one pressure moment and its outcome is presented at a time. Ledger, shot controls/court, 14-record list and raw codes are concealed in closed, named native disclosures until requested.
- All 3 audited moments, all 20 shot fragments, every included comparison point and all 14 game records remain inspectable. Counts, source fields and hash match original records. Explicitly say the 3 selected moments are not consecutive; keep point-vs-shot and causal limits.
- Browser checks at desktop/tablet/phone/crowded landscape: next/back, source disclosure, exact keyboard focus, touch, reduced motion, no overflow, no invisible active controls. No-script supplies readable comparison/outcomes and source access. Preserve direct-file loading.
- Measure local load and transition work; review rendered results. Independent completed-change review before reporting. Durable report records actual observations separately from untested comprehension.

Next: user assessment of the simplified path; implementation work and local verification are complete.

Editorial refinement before final verification: essential point outcomes stay visible with their current moment. Removed the extra reveal step; the sole primary action advances to the next selected moment. Source disclosures remain opt-in.

## Delivered change

The main path now contains one service-point comparison, one current pressure moment/outcome, and a short conclusion. It has no mandatory 3D scroll sequence, revealed-results panels, serving filter, complete point table, moment tabs, portraits or stroke court visible by default. The current moment has one primary Next action and a secondary Back action after the first moment. Native disclosures provide the comparison ledger, stroke diagram, complete 14-point game and methodology when requested. The 14-point inspector is independent: examining an omitted point cannot change the story's current score or moment. Next/back closes optional moment detail, and all set-point links reset to source150.

Active main controller/styles: reader.js/reader.css, replacing the loaded demo.js/portrait controller. Exact existing comparison/shot modules and frozen data are retained. The unused older controllers/assets were not deleted from the user's existing untracked work. Main game colour, serif voice and score orientation remain. No new image, dependency, model, case, external call or infrastructure.

## Verified results

- Independent original-CSV verifier passes. Frozen 110-record SHA-256 unchanged. All primary fractions, complete cohort memberships, counter-drop evidence and source fields still match the original specimen. No new source-derived claim was introduced.
- **1,603 new-flow browser assertions pass** at 1440×900, 768×1024, 390×844, 320×568, 844×390, 900×700, 640×450 and 1024×600. They cover default closed evidence, one primary action/current moment, exact three score states, all 20 audited stroke fragments and alternating actors, original fields for every comparison point and all 14 game points, independent optional inspection, Next/Back/opening/skip/revisit routes, keyboard focus and Tab continuation into requested evidence, emulated touch, reduced motion, source access without script and direct-file startup. Page overflow was checked with raw records expanded. Scripts/results: ignored reports/discovery/focus-journey/verify.mjs and checks.json.
- Current desktop/tablet/phone/crowded screenshots were inspected for opening, current outcome and opted-in shot details. The main reading column leaves the 14-point list and court out of view until requested. Optional horizontal stroke scrolling is retained inside the requested inspector. No claim of physical-device or assistive-technology testing.
- Six cold-context Chrome runs, three each at 1440×900 and 390×844, measured 90 moment transitions per run (540 total). Synchronous transition-call p95 was 1.5–2.2 ms; frame-interval p95 was 16.7–16.8 ms; no measured interaction long tasks. Default game has 3 visible controls at the first moment: one primary Next plus two native evidence summaries. Initial resources were 243,214 bytes in repeated runs (first run adds 460 bytes for favicon); no image requests. DCL ranged 26.5–69.8 ms, too local/variable for a speed claim. Exact executable method/raw samples: performance.mjs/performance.json. No comparison against the previous UI's structurally different interaction timing is claimed.
- Independent review verified source semantics, default disclosure state and the replacement flow. It identified two route/focus defects: source links scrolled to the ledger without moving focus, and named set-point links retained a later selected moment. Both were fixed and explicitly tested. Final re-review reports no remaining actionable issue. The old 34,986 simultaneous-layout suite was not presented as verification of this replacement.

The mechanical design detector ran once. It flags the inherited ivory/italic/Arial identity, type steps and a full-width dark section as a generic cramped-container warning. Rendered screenshots show a centered 720px column with ample inset; the secondary surface deliberately contains a court diagram, not a decorative grid. These advisories do not establish audience usability. Context tooling also found legacy product metadata/stale design sidecar; no unrelated metadata migration was made (init/document would own that separate maintenance).

## Limits and durable state

This change responds directly to actual user feedback about competing simultaneous elements. The reduction in default controls and concealed inspector state is verified. Improved comprehension, curiosity and satisfaction remain judgments to test, not measured outcomes. No fresh fan session, real screen-reader session, physical phone or other browser engine was used. Exact remaining reader observation: can a fan follow the current moment and explain the 11/11 versus 1/5 comparison without opening an inspector, then find a source record when they choose to check it?

HEAD remains 2c40e40c0f3ac51cc11eabe6c7c25932234e83e0 on branch codex/fan-evidence-journey. Main index/README changed; reader.js/reader.css added. Upstream CSVs, models, original data, unrelated deletions/untracked files and historical implementation files preserved. Task record updated. No commit, merge, publishing, install, paid use or external contact. Local 8765 preview remains available.

Native in-app preview was refreshed and walked from the opening into set point, then game point; current text and heading focus update correctly. The user preview is retained.
