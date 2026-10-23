# Two ways forward — Margins

The restored court-led reading of Djokovic’s second set against Medvedev in the 2023 US Open final: open the tactical results, test the serving scope, inspect the complete comparison, then explore three pressure moments and the full 14-point game.

From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory gui/margins-experiment
```

Open [the study](http://127.0.0.1:8765/tactical-demo/). Direct-file opening also works. No build framework, API, account or external dependency is required.

## Current interaction

Scroll directly splits and flattens the court. Its equal pieces name categories; area is not a quantity. Reveal the results and keep Djokovic’s service points: drop-shot points move from 3/11 overall to 1/5 on serve, while serve-and-volley remains 11/11. The ledger exposes every point behind both fractions, its pre-point score and winner, with raw notation under explicit source disclosures.

The pressure game retains the neutral portraits, three moment controls, readable stroke selector and categorical court. Exact source fragments remain opt-in. Arrow keys, Home/End, direct selection and ending shortcuts work; each moment remembers its inspected stroke. All 14 game points remain accessible in the stable inspection frame. Portrait emphasis is identity/hitter feedback, not a player reaction or measured position.

The single-moment reader was rejected and reverted. `reader.js` and `reader.css` are removed. `demo.js`/`demo.css`, `comparison.js`, `pressure-shots.js`, `shot-sequence.js` and `player-portraits.js` are the active controllers/styles. The final polish preserves this architecture, improves destination focus, tightens stroke-card spacing, shortens ending shortcuts, and serves responsive derivatives of the same artwork. Original 1254px images and their hashes remain unchanged.

System or explicit reduced motion keeps evidence static. Crowded landscape views use normal document flow. No-script copy and the complete source download remain available.

## Evidence

`source-points.json` preserves the 110 original-format second-set MCP records. The frozen SHA-256 is `eb6f8cf0b7c3766f92f70424d9ec870a79a325e06360b4cba67b5444e62b1b5e`. `data.js` adds audited tactical memberships. No model, prediction feature, upstream CSV or original field changed.

The three shot views are source150 (5 strokes), source154 (13 counted strokes, preceding let excluded) and source155 (2 strokes; missed return, no volley). Bands show charted direction categories, shading a receiving service box or documented completed-return depth. No measured locations, trajectories, timing, causal tactic effect or psychological state is claimed. Full-game omissions, counter-drop84 and the whole-match source disagreement remain inspectable.

Data: Jeff Sackmann / Tennis Abstract Match Charting Project, charted by Zindaras, CC BY-NC-SA 4.0. Font OFL and generated-asset provenance are retained. Responsive asset hashes/method are in assets/portrait-responsive-derivatives.json.

## Release

```sh
python3 scripts/build_study_release.py
```

This produces the linked two-study static site under reports/releases/margins-static/ and its ZIP/hash file. Tactical entry: `/tactical-demo/`; Wimbledon: `/`. No backend or private files are included. [Deployment instructions](../../../docs/deploy_static_studies.md).

Current restoration, polish, packaged-browser verification and independent review: [release report](../../../docs/research/2026-10-23-restore-polish-release.md). Previous focused-reader reports are historical and superseded. No public hosting has been configured or activated.
