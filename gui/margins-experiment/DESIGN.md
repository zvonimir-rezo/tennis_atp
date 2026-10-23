---
name: Margins — The anatomy of almost
description: A sculptural grass court opens an exact historical point investigation.
colors:
  paper: "#eeeade"
  ink: "#173c30"
  plum: "#5d2945"
  muted: "#536057"
  filter-bg: "#dedfce"
  filter-hover: "#ced4bc"
  filter-selected-hover: "#285242"
  source-bg: "#dfdfcf"
typography:
  display:
    fontFamily: "Instrument, Georgia, serif"
    fontSize: "clamp(88px, 11.4vw, 184px)"
    fontWeight: 400
    lineHeight: 0.88
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Instrument, Georgia, serif"
    fontSize: "clamp(58px, min(6.3vw, 10svh), 100px)"
    fontWeight: 400
    lineHeight: 0.88
    letterSpacing: "-0.035em"
  section:
    fontFamily: "Instrument, Georgia, serif"
    fontSize: "clamp(60px, 6vw, 96px)"
    fontWeight: 400
    lineHeight: 0.88
    letterSpacing: "-0.035em"
  body:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "16px"
    lineHeight: 1.5
  count:
    fontFamily: "Instrument, Georgia, serif"
    fontSize: "66px"
    fontWeight: 400
    lineHeight: 1
  label:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "12px"
rounded:
  square: "0"
  circle: "50%"
spacing:
  desktop-gutter: "5%"
  section-gutter: "7%"
  phone-gutter: "6%"
  filter-gap: "8px"
  phone-filter-gap: "6px"
components:
  filter:
    backgroundColor: "{colors.filter-bg}"
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
    padding: "10px 15px"
  filter-hover:
    backgroundColor: "{colors.filter-hover}"
  filter-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  filter-selected-hover:
    backgroundColor: "{colors.filter-selected-hover}"
  point-input:
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
    padding: "7px"
    width: "72px"
  text-action:
    textColor: "{colors.ink}"
    padding: "0"
---

# Design System: Margins — The anatomy of almost

## Overview

**Creative North Star: "The anatomy of almost"**

The approved world is a sculptural grass court suspended over warm ivory: raking light, deep shadow and oversized editorial type. One continuous object separates into five categorical set sections, then yields to the exact point record. The metaphor supplies material and continuity; the persistent marks supply evidence.

This visual system applies only to the disposable historical study in this folder. The user-approved replacement in [REDESIGN.md](REDESIGN.md) supersedes the earlier dark ledger identity. Its dramatic sports editorial voice serves the bounded investigation in [PRODUCT.md](PRODUCT.md): an authored claim readers can inspect and challenge.

**Key Characteristics:**

- A material court over warm ivory, with thin chalk geometry and structural shadow.
- Instrument Serif at sporting scale, paired with plain supporting text.
- Equal tennis-ball pictograms, dark green for Federer and plum for Djokovic, with persistent record identity.
- Continuous, reversible scroll; immediate inspection; static reduced-motion chapters.

## Colors

Warm ivory carries the court and the argument; dark green and plum maintain the two player identities.

### Primary

- **Court ink:** the dark green text, Federer marks, selected filters and verdict ground. Turf has its own authored image variation rather than a single flat color token.

### Secondary

- **Opponent plum:** Djokovic marks and totals, selected-record context, wordmark punctuation, focus outlines and current chapter marker.

### Neutral

- **Warm ivory:** the page ground, pale court overlay, inverse text and focus-label backing.
- **Muted green grey:** metadata, sample denominators and supporting labels.
- **Quiet filter surfaces:** neutral resting and hover states; selected hover uses a deeper green.
- **Source paper:** the slightly darker closing source section.

**The Stable Identity Rule.** Federer stays dark green and Djokovic stays plum. Equal ball bodies have curved seams (Djokovic’s seam is rotated); names and explicit F/D winner lanes carry identity without relying on tiny seam details.

## Typography

**Display Font:** Instrument Serif Regular and Italic, locally aliased as `Instrument`, with Georgia and serif fallbacks. Both assets come from the official [Google Fonts source](https://github.com/google/fonts/tree/main/ofl/instrumentserif); the OFL is retained in `assets/OFL-InstrumentSerif.txt`.

**Body Font:** Arial, Helvetica, sans-serif. Source code uses the browser monospace face.

The regular/italic relationship supplies an editorial voice. Headline scale is dramatic; exact samples and definitions remain plain. Numerical evidence is never animated as a count-up.

### Hierarchy

- **Display:** the frontmatter opening role; the italic second line carries the turn in the title.
- **Headline:** the compact stage role. The verdict uses `clamp(76px, 8vw, 128px)`; inspection and source titles use the section role.
- **Body:** base frontmatter role. Opening copy is 18px/1.45 at 32ch; compact copy is 16px at 32ch. Inspection introduction is 18px at 26ch. Supporting text and controls range from 12–16px.
- **Count:** the frontmatter full-match total role. Group margins are 64px/.9; the balanced remainder pair becomes 64px/.9. Record scores are 58px/.9. Count fields use tabular numerals where implemented.
- **Label:** the frontmatter metadata role; group actions are 16px and winner counts 13px on desktop.

## Layout

The opening retains a full viewport editorial stage: title upper left, court lower/right, whole-match totals lower left. Analytical chapters use separate narrative, legend, evidence and footer bands. Desktop compact type is `clamp(58px, min(6.3vw, 10svh), 100px)` with .92 line height; explanatory copy occupies the opposite upper corner. The evidence field has 5% side gutters, top `clamp(260px, 34svh, 380px)`, and 110px bottom clearance. The legend is 46px above it. Group labels, record lanes and court surfaces derive from shared rectangles; slab origins are top left. Five-set sections have equal dimensions. Later group surfaces fit their contents; their area is not a quantitative encoding.

At width ≤760px, evidence gutters are 7%, the compact title is `clamp(44px, min(13.4vw, 7.4svh), 72px)`, and explanation follows beneath it. The evidence field begins at `clamp(258px, 35svh, 330px)` and ends 108px above the bottom. Set two occupies the left 35%; the complementary groups stack in the right 57%, separated by an 8% gap. At height <740px the field begins at 188px and ends 100px above the bottom, the compact title is 44px and explanation is 12px. Five-set samples show fractions; the nearby legend defines the point unit. No quantity is omitted. Text-ink bounds, rather than line boxes alone, determine clearance above the first ball row.

The 850×420 object plane is internal geometry. Resize measures the evidence field’s actual fractional bounds; scroll consumes cached values. The camera is fully flat by the five-set stop (.38), so all analytical surfaces align with their own data. Verdict, inspection and source sections retain the existing responsive composition.

## Elevation & Depth

Depth is structural: five CSS 3D court slabs, turf, exposed earth edges, chalk linework and a raised net. A blurred offset floor shadow anchors the object above ivory; the point evidence and controls stay flat. Flattening and pale surface overlays make the categorical point arrangements readable while preserving the held set-two object. No WebGL, canvas renderer, framework or animation library is used.

### Shadow Vocabulary

- **Floor shadow:** a dark green oval (`filter: blur(18px)`) whose opacity and transform follow scroll; phone blur is 15px. It anchors the court, not a UI card.
- **Turf inset:** `inset 0 0 24px #153c2625` adds material edge depth.
- **Focus:** an immediate plum outline (2px, 5px offset), separate from object lighting.

**The Symbolic Court Rule.** Equal court sections name sets. Their area never encodes point totals, elapsed time or shot locations.

## Shapes

The court has square slab edges, exact SVG linework and a CSS net. Each persistent record is a native SVG group containing an equal-radius disc (5.5 units) and one simple seam path. Desktop effective diameters range from 6.49–11px, depending on width and height; phone diameters are 6.05px, or 4.95px below 740px height. Pitch is bounded above the diameter, with explicit winner lanes and equal sizing within each viewport. There are no per-ball filters, gradients or shadows. A record halo appears only after intentional point selection; arrival and subset selection alone create no arbitrary highlight. Controls remain rectangular.

**The Equal Unit Rule.** One persistent keyed mark equals one recorded point. Arrangement changes coordinates, never winner, identity, equal mark area or the denominator of 422.

## Components

### Sculptural court and record field

The grass is an image-generated material, not a photograph of the 2019 court. Its [provenance](assets/grass-turf-provenance.md) and [prompt sidecar](assets/grass-turf.webp.json) remain beside the WebP. Court lines, geometry, depth, net and light are browser-rendered. Only the 422 persistent native SVG point nodes are match evidence. Set two retains its 38 records (IDs 88–125); the other four total 192–192, then divide into 33 tiebreak points (12–21, −9) and 351 other points (180–171, +9).

Scroll is a direct, reversible playhead: stopping holds the composition and scrolling back retraces it. Event-driven `requestAnimationFrame` paints the current scroll position; there is no autonomous timer or WAAPI runtime. Smoothstep interpolation is `t²(3−2t)`. Chapter controls jump immediately to scroll stops 0, .38, .61, .86 and 1. Exact changing-group labels are hidden during travel; set two’s stable label remains during the final split. The old `app.js` is not loaded by this page.

### The concentration handoff

The 2026-10-22 scroll refinement changes only the five-set → concentration transition. Set two moves over playhead .43–.49 and then retains exact coordinates. The remaining 384 records assemble over .43–.575. Its fixed 38/422, F26/D12, +14 label returns only once the remaining transfer is at least .85, clearing foreign records from that surface. The other-four-set readout remains hidden until its records land.

The existing headline slot briefly says “Hold set two. Watch the rest.”, with an instruction to follow the four sets. Exact 192–192 becomes inspectable at .575; “All fourteen. In one set.” arrives at .605. This .03 playhead span lets evidence precede the conclusion without a forced wait. It adds no chapter or control. Keyboard chapter jumps and reduced motion still land directly at the complete .61 stop. Existing smoothstep interpolation, native SVG transforms and transform/opacity rendering remain; no spring, timer, library or per-frame geometry read is introduced. Every intermediate state reverses from the current scroll position.

### Chapter navigation and motion setting

Five accessible buttons form a vertical dot track at desktop right; the current dot becomes a plum line. Focus or fine-pointer hover reveals a label. Phone uses a horizontal line track near the stage bottom. Buttons have a 44px minimum height. The quiet underlined motion action shares the footer, not a detached control panel.

System or explicit reduced motion hides the 3D scene, collapses the long scroll section and provides static named evidence through the chapter controls. The explicit toggle retains the current chapter (opening resolves to the verdict); when collapse occurs while inside the stage, it returns the viewport to the opening stage so the composition remains in view. Returning to full motion restores the matching chapter stop. System reduction disables the explicit control. On short phones, the reduced-mode masthead enters normal document flow so it cannot overlap the title; ordinary scrolling reaches the complete static composition. Records and inspection remain available.

### Group labels and inspection

Named group buttons expose sample count, signed margin and winner totals. Activation opens the exact subset in inspection and focuses the point field. Green/plum ball legends and explicit F/D lanes make identity clear. Subset filters are flat rectangles; selection inverts to ink over ivory, with independent hover colors. Context marks dim to .35 rather than disappearing.

The numeric point field is 72px wide with a bottom rule, a 44px minimum height and tabular numerals. Previous/next arrows, named shortcuts and literal source fields provide record access without 422 tab stops. Left/right in the details step through the selected subset; Escape returns focus to the field. The full denominator and pre-point Federer/Djokovic score orientation stay visible. All inspection changes are immediate.

### Editorial closing sections

A dark green verdict reverses the type to ivory. The following open inspector and quiet source-paper section retain generous insets and typographic hierarchy, without raised cards. The source section carries attribution and limits in the reader’s path.

## Do's and Don'ts

### Do:

- **Do** preserve the approved ivory, turf, raking-light and deep-shadow world.
- **Do** keep exact totals, subset denominators and the strongest objection inspectable.
- **Do** hold set two in place while the other four sets divide into opposing −9 and +9 margins.
- **Do** treat screenshots as captured page frames; state viewport measurements separately and exclude browser chrome from the image frame.
- **Do** use the static chapter path for system or explicit reduced motion.

### Don't:

- **Don't** restore the superseded dark ledger, acid accent or compressed Barlow headline identity.
- **Don't** mistake the illustrative court or generated grass for match evidence.
- **Don't** add invented trajectories, elapsed clocks, count-ups or interpolated evidence totals.
- **Don't** infer psychology, deservedness or a match without set two.
- **Don't** treat browser assertions or a scoped finish review as proof of demand, reader learning or physical-phone performance.

## Scroll rendering contract

Resize and motion-preference changes own dimension measurement; scrolling owns a direct reversible playhead with no timed tail. Each of 422 SVG record groups retains a native translation and scale. Unchanged points/content stay stable, and set two uses explicit held coordinates during the complementary split. The 2026-10-22 composition revision preserves this optimized hot path while adding two static child shapes per record. The material court remains intact on opening; its floor shadow fades as the object becomes a flat evidence diagram. Pale surfaces and structural green top edges clarify the analytical state without a duplicated grass texture behind fine marks.
