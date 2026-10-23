# Illustrated players and recorded hitter

Implemented the user's requested artwork and active-hitter treatment in the existing local Djokovic–Medvedev demo. The bold green/plum portraits give the pressure section a recognisable player identity; smaller versions above the shot court make each recorded hitter legible while stepping through the point. The original sculptural court split and evidence comparison remain intact.

## Artwork and interaction

Generated two transparent1254×1254 editorial cutouts with the built-in image tool. They use flat inks, carved shapes and screenprint texture against the existing US Open blue. Both show a fixed neutral expression. Assets and full prompt provenance are saved under `gui/margins-experiment/tactical-demo/assets/`. These are identity illustrations, not photographs or evidence of a match event. A generic authored SVG racket identifies the hitter without implying a swing or position.

The pair enters once on first visibility:240ms,40ms stagger, existing ease-out,24px translation and slight opposing rotation. Backwards fill holds the delayed illustration at its first keyframe. Keyboard-first entry is immediate. Pointer shot changes use120ms opacity/scale emphasis; keyboard changes are immediate. System/explicit reduced motion uses100ms entrance fades and80ms hitter fades, with no transform. Preference changes cancel running entrance motion. Native CSS/WAAPI only; no dependency.

Portraits sit outside the shot SVG. `shot.actor` alone controls the active state. All20audited tokens, actor identities, source fragments and categorical court regions remain unchanged. No player coordinates, ball paths, invented timing or emotional reactions were added. Source110-record JSON SHA-256 remains `eb6f8cf0b7c3766f92f70424d9ec870a79a325e06360b4cba67b5444e62b1b5e`.

## Review and verification

- Independent source review passed the actor integration, evidence boundaries, motion/input preferences and accessibility labels. Final small label/heading/stagger fixes were independently reviewed again. Audit: `reports/discovery/tactical-demo/portrait-source-audit.json`.
-1052shot-view browser assertions passed across1440,768,390,320and1200px widths, including exact tokens/actors, bounded categorical court display, focus, source guards and reduced motion.
-42motion checks passed across four widths plus system-reduced and keyboard-first pages. Native pointer and keyboard input verify transition behavior and once-only entry.
-532existing-flow regression assertions passed across five viewports: unchanged110records, original partitions and denominator changes, all14game points, court-split reversal, focus and reduced motion. Direct-file/font test passed.
- Final artwork/layout checks passed at1440,768,390and320px: all assets loaded, no horizontal overflow, no clipped hitter rows,13pxminimum new labels. The phone heading uses one line to keep the introduction compact. A screen-reader heading label preserves the word boundary.
- Final browser layout inspector reports0findings at1440/768/390with the declared inherited typography, palette, court-mesh and content exceptions. Final page sheets and dedicated portrait views were inspected. The separate raw source style-detector output is retained as `portrait-design-detect.json`; inherited stylistic advisories are not represented as a clean detector pass.
- Native in-app-browser stepping changed the active face and racket label to Medvedev on his recorded return. The finished preview is left at the pressure section.

One offscreen lazy-image decode timeout occurred in the initial screenshot probe. Eager loading fixed it; the single recovery passed. No further identical retry was needed. Before-source copies, probes, screenshots and raw results remain under ignored `reports/discovery/tactical-demo/portrait-*`.

## Scope and limits

No reusable case engine, upstream CSV/model edit, dependency, paid API/CLI fallback or publishing. Existing unrelated working-tree changes remain untouched. Branch `experiment/margins-ledger`, HEAD `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`; no commit made. Browser checks establish faithful interaction and rendered layouts, not audience appeal, exact portrait likeness or physical-phone/cross-browser certification. The user can now assess whether the stronger player identity improves the discovery.
