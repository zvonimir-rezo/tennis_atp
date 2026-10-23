# Two ways forward — small tactical demo

Delivered 2026-10-22 at local prototype scope. Question: does the Djokovic–Medvedev second-set contrast feel worth investigating when readers can split the court, challenge the denominator and step through the actual 5–6 game?

Preview: http://127.0.0.1:8765/tactical-demo/. Source: `gui/margins-experiment/tactical-demo/`. Run instructions and source fingerprints are in its README. Existing Wimbledon files are unchanged. This is explicitly case-specific code, not a reusable case system or production integration.

## What was built

- A blue CSS 3D hard court over the established Margins ivory/Instrument Serif world. The court splits into three equal categorical pieces and flattens into the evidence. No physical shot location or trajectory is invented.
- Exact Djokovic-service groups: 11/11 serve-and-volley, 1/5 own-drop-shot points, 25/36 other points. The whole-second-set toggle gives 11/11, 3/11 and 44/88. All counts derive from the frozen original-format records, with explicit research-audited memberships.
- The complete fourteen-point 5–6 service game, with pre-point score, outcome, source ID and raw record. Native controls/arrow keys step all points; pattern controls highlight without removing context. A set-point shortcut goes to150 and moves keyboard focus to that point.
- Source access to all110 second-set records, including counter-drop84 and player-order score normalization for Medvedev serves and tiebreaks. The full-match official/MCP classification disagreement remains explicit.
- A bounded verdict: the contrasting outcomes describe this set and these opportunities; they cannot establish what another shot choice would have produced.

The main pointer action uses native interruptible smooth scrolling through the dissection. Scroll position otherwise directly determines the physical transforms, with no timed animation controller. Keyboard/chapter actions and scope/point changes are immediate. System/explicit reduced motion uses a static split and ordinary page scrolling.

## Verification and independent review

**447/447 browser assertions passed** at1440×900,768×1024,390×844,320×568 and1200×700. Checks include exact110 source rows and persistent mark IDs; complete game143–156; both scope totals and visible denominators; mark/text clearance and bounds; reversal/intermediate progress; all fourteen pre-point scores and original records; pattern membership; native keyboard stepping/focus; corrected serve narration; source orientation including tiebreaks; explicit/system reduced motion; restoration to full motion; and no runtime exceptions. Diagnostic script/log: ignored `reports/discovery/tactical-demo/verify-browser.mjs` and `browser-verification.json`.

Direct-file opening also passed:215-derived110 source records,14 game points and local Instrument font loading. JavaScript syntax and retained-source SHA-256 checks passed. Native in-app-browser scope controls, ordinary scrolling and pointer primary action were exercised. Browser evidence is Chromium at emulated CSS viewport sizes, not physical-phone or other-engine certification.

An independent researcher checked the unchanged records, hashes, classifications, all game states, faulted approach145, double faults146/148, set-point save150, drop154 and source orientation. It found one narration error:144 was called a second-serve rally. The description was corrected to first-serve rally and independently rechecked. Audit status: pass. Later changes concern layout, visibility and focus; they do not alter records/memberships. Audit: ignored `independent-evidence-audit.json`.

Rendered review: desktop opening/split/game and phone/short-phone/reduced frames inspected. Increased small labels, moved navigation out of the court, cleared phone copy alignment, labeled scoreboard values, kept the strongest counterexample visible, and shortened the pinned sequence to220svh. Final images: ignored `final-<width>-opening.png`, `-split.png`, `-game.png`, `-reduced.png`.

## Design-tool results and limits

The established sculptural/serif world was inherited rather than rerolled; the user explicitly requested retaining the court splitting. Impeccable's mechanical scan returned contextual warnings about the inherited italic/cream/Arial identity, the physical net grid and the new hard-court/tinted labels. The flagged wide-section padding is a percentage-inset false positive: actual desktop72px/phone23px gutters are visible in captures. Small readable captions were raised to13px; source code is optional inspection content.

Taste inspection at1440/768/390 reports no runtime errors or horizontal overflow. Declared exceptions cover the inherited serif/cream system, scoreboard/point-context labels, actual-source monospace, responsive numerical sizes, the physical net's grid and the absence of photographs/footage in this data-and-court demo. No extra imagery was introduced to satisfy a marketing-page picture quota.

Two raw heuristics remain outside the declared exceptions: `pinned-over-picture` treats a count over its own symbolic court plate as a picture collision, although the mark field begins below the count and all mark/text clearance checks pass; `empty-screens` fails to count the CSS3D object/plates as graphical content. Visual captures show the court and plate field occupying the intended stage. A pixel check against the paper ground with2% color tolerance finds **27.25%** non-paper pixels in the desktop opening and **42.48%** in the desktop split, rather than an empty composition. These raw scanner findings are retained, not presented as a clean generic style certificate.

The parent's older PRODUCT schema and DESIGN sidecar drift remain separate; optional `init`/`document` maintenance was not run as part of this demo. No website publication, service installation, model/source CSV change or new paid usage occurred. HEAD remains`2c40e40c0f3ac51cc11eabe6c7c25932234e83e0` on`experiment/margins-ledger` with existing unrelated changes preserved.

The demo is ready for the user's qualitative judgment. Neither the assertions nor these screenshots establish audience surprise, enjoyment or a reason to build the reusable system.
