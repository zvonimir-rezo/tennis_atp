# Margins implementation: independent evidence and controller review

2026-10-21. Reviewed `gui/margins-experiment/{index.html,app.js,records.js,style.css}` against the motion evidence audit and design/motion specification. No application files changed and no browser process launched. This is a source/evidence review; actual browser timing, visual continuity and assistive-technology output require the separate browser review.

## Verified evidence

An independent Python standard-library recount parsed the retained JSON directly, compared every embedded record with that raw source, verified SHA-256 `b772afeb9e76baa3f0c7c21c0351ae72dddfcf47afe2111378b6bfeb720e89f3`, and checked all 422 unique `(match_id, Pt)` identities and sequential ordinals. Embedded records are exact copies. A fresh scoring replay, without using raw set/game fields to advance state or classify groups, matched all 422 pre-point `Set1`, `Set2`, `Gm1`, `Gm2`, `Pts`, `Svr`, and `Gm#` values. It ends Federer/Djokovic 2–3 sets, with game scores 6–7, 6–1, 6–7, 6–4, 12–13.

Independent counts agree: whole match 218–204/422; five sets 41–46/87, 26–12/38, 37–36/73, 30–25/55, 84–85/169; other four sets 192–192/384; three breakers 12–21/33; neither set two nor a breaker 180–171/351. The 38/33/351 groups are pairwise disjoint and cover exactly all identities. Point 81 normalizes correctly to Federer 2 / Djokovic 3; points 359/360 normalize to 40–15/40–30 with Federer serving, Djokovic winning, outside the breaker group. No evidence-identity, denominator, score-orientation, causal or novelty overclaim blocker was found in settled-state source logic and copy.

## Findings and follow-up

Both original P2 findings were addressed in the implementation during this review:

- **Resolved in source — Source-label and selected-38 continuity.** `go()` retains departure context until `settle()`, with an explicit moving-state caption identifying the departure arrangement. A visible frame tracks set two on the shared animation clock; literal IDs 88–125 are provided in the departure context for the focal edge. Reverse plays those same animations backward; arbitrary retarget cancels old animations and derives the new point/frame source from current computed mark positions. This addresses the original omission in source. Actual perceptual continuity remains a browser observation.
- **Resolved in source — Aria-hidden interactive group labels.** `#group-labels` no longer has `aria-hidden="true"`; its named buttons can participate in the accessibility tree. Screen-reader behavior remains a browser/assistive-technology check.

**Resolved in source — Focus through group-control replacement.** `drawLabels()` now captures the focused group's stable key before replacing labels and restores the corresponding destination control, falling back to the persistent Next control when that group has no destination counterpart. Group activation deliberately transfers focus to the point input after scrolling to inspection. This addresses the previously reported detachment hazard. The parent separately reports browser verification of these focus paths, Enter activation, point stepping and Escape; this independent review did not launch a browser.

Final regression pass: moving Pause/Replay before the chart, phone DOM reparenting with active-element restoration, heading focus after phone advance, and the larger chapter-two label allowance introduce no evidence, source-label or reverse/retarget regression found in source. `settle()` also restores focus when it disables a focused Pause control.

**Resolved in source — Pause during resize.** Playback-focus recovery is now centralized in `updateStatus()`, so both `settle()` and instant `go()`/reflow recover a focused Pause control before it remains disabled. It selects Replay when available and otherwise the persistent Next control.

The final departure-context revision preserves the source groups, ID-derived counts, denominators and margins outside the travelling marks. During travel, the original in-plot label controls are hidden; a previously focused group control transfers to Pause. The full-match 218/204 and 422 summary remains in the header. The selected-38 spatial frame stays on the shared animation controller. Reverse retains explicitly named departure context, and settle reveals destination labels. No remaining material evidence, source-label-conservation, focus or reverse/retarget defect was found in this final source pass.

No source-review blocker remains for this bounded experiment. This does not certify appearance, performance, assistive-technology output or fan comprehension.

## Controller assessment and remaining checks

The controller reads actual computed mark positions before cancel/retarget; it cancels old finish handlers, uses a token guard, shares timing, reverses an existing uninterrupted edge, settles before record/subset inspection, retains the focused record through chapter changes/reflow, pauses on hidden-tab notification, and settles on live reduced-motion activation. These are appropriate source-level mechanisms. No stale-completion or record mutation bug was found.

The revised shared `pauseAll()` captures one animation time and assigns it to every paused animation, including the transfer frame/label; hidden-tab pausing uses that same function. This removes individual pending pause offsets at source level. The parent separately reports browser freeze/reverse checks at 80/400/700ms. The revised transition-label treatment explicitly distinguishes retained departure context from the requested destination during forward, reverse and retarget operations. Inspection of the updated controller found no additional material reverse/retarget defect. Native WAAPI finish/reverse behavior, pause timing, five rapid direction changes, live preference changes, focus continuity and visual record conservation still need the parent’s browser exercise. No runtime-performance conclusion is made here.
