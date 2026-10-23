# Pressure points150,154,155: what can honestly go on the court

Independent evidence review, 2026-10-23. Scope: decode three frozen USOpen2023 final records for a proposed on-court view. No application files changed. Djokovic is source player1 and serves all three points; Medvedev is player2. Both are right-handed in retained MCP match metadata. Source rows are unchanged in [the demo specimen](../../gui/margins-experiment/tactical-demo/source-points.json), match `20230910-M-US_Open-F-Novak_Djokovic-Daniil_Medvedev`.

## Recommendation

Use the court to show **categorical serving halves, recipient-relative direction bands and a generic net-error state**, accompanied by a numbered actor/shot sequence. Do not turn these codes into dots at landing coordinates, moving player positions or a connected ball-flight animation. The source provides no measured launch, contact, bounce or net-crossing coordinates and no elapsed timing, height, speed or flight curvature. Court ends in a fixed diagram are a chosen orientation, not a recovered camera view.

The decisive source detail is that **direction1/2/3 describes the part of the opponent's baseline the shot crossed or would cross**. It does not locate the bounce. A ball may bounce centrally yet be coded1 because of its projected direction. This is explicit in the primary workbook Instructions **A134–A136**, rather than an inference from tennis convention. Therefore a full-length band labelled “toward opponent's backhand side” is a schematic directional category; a filled rectangle labelled “landed here” would be false precision. [Primary workbook](https://github.com/JeffSackmann/tennis_MatchChartingProject/blob/master/MatchChart%200.3.2.xlsm).

## Primary decoding contract

Inspected the retained [MatchChart0.3.2 workbook](../../reports/discovery/case-search-tactical/MatchChart-0.3.2.xlsm) and its extracted shared strings. Cell references below refer to the actual Instructions worksheet. Workbook SHA-256: `46e2349eee512296a86170449f6e463a6be91be9261a0c7b6b5d5a25c006729f`.

| Code | Meaning and evidence |
| --- | --- |
| `4`, `5`, `6` at serve start | Wide, body and T serve categories; same meanings on ad/deuce sides. InstructionsA47. |
| `+` after serve | Serve-and-volley attempt; it records an approach, not a measured running route. InstructionsA70–A72,A187; also author's [quick start guide](https://www.tennisabstract.com/blog/2015/09/23/the-match-charting-project-quick-start-guide/). |
| `c` before serve | Service let, not a stroke or change of actor. InstructionsA61,A68. A repeated let can repeat `c`. |
| `f`,`b`,`z`,`y` | Forehand groundstroke, backhand groundstroke, backhand volley, backhand drop shot. InstructionsA96–A97,A103,A110. |
| `1`,`2`,`3` after shot | Toward recipient's right-hander forehand side, middle, right-hander backhand side. InstructionsA126–A128. Both recipients here are right-handed. These are recipient-relative, not absolute screen left/right. |
| `*` | Winner marker on final shot. It does not reveal its coordinates. InstructionsRallyEndings. |
| `n`,`w` with final error | Net error, wide error. Wide may be either direction; it does not give the out-of-court coordinate. InstructionsA52,A155–A163. |
| `@`,`#` | Charted unforced/forced error classifications. These describe the chart, not an independently estimated psychological or causal mechanism. InstructionsA155–A163. |

The [MCP dictionary](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/data_dictionary.txt) defines player order, score state, server, winner and the first/second-serve cells. A nonempty `1st` containing the entire rally with empty `2nd` means the active rally follows a first serve. All three examples do so; point154 has a preceding service let rather than a first-service fault.

### Depth: distinguish documented returns from extra rally digits

InstructionsA173 defines return-depth categories: **7** in the service boxes; **8** behind the service line, nearer it than the baseline; **9** nearer the baseline. The surrounding section explicitly concerns **in-play service returns**, and the author's [quick start guide](https://www.tennisabstract.com/blog/2015/09/23/the-match-charting-project-quick-start-guide/) likewise introduces depth for returns.

The current raw record contains extra7/8/9digits on later shots, including `z38` and `z29*` in point150 and many groundstrokes in154. The retained0.3.2 Instructions does **not** establish a general rally-depth grammar or explain depth on volleys. Thus:

- The first return `f39` in154 has documented direction3 and return-depth9: a deep forehand return toward Djokovic's backhand-side direction. A coarse depth category is available here; an exact landing point is not.
- `z38` and `z29*` have verified shot type and first direction digit. Their extra8/9 are retained in the raw code but should not be presented as independently verified volley landing depths on the strength of these Instructions alone.
- `f39w#` in155 is a **missed** return. Its direction3 and wide/forced-error classification are clear. Although9occupies the depth-like numeric position, the documented depth section concerns in-play returns. Do not use it to claim an in-court deep landing; retain the raw9or label depth unavailable for this error unless a newer primary grammar is established.

This is a limitation of the documentation verified here, not proof that the extra digits are meaningless or that no later convention exists. Do not silently discard them from source access or invent an authoritative interpretation to draw a more detailed replay.

## Exact point150: set point saved

Before: Djokovic serves at games5–6, points40–AD. Raw `1st`: **`6+f3z38b3z29*`**; `2nd` empty. Djokovic wins.

| Attempted stroke | Actor | Raw token | Verified description |
| --- | --- | --- | --- |
| 1 | Djokovic | `6+` | First serve down theT, followed forward. |
| 2 | Medvedev | `f3` | Forehand return toward Djokovic's backhand-side direction. No return depth recorded. |
| 3 | Djokovic | `z38` | Backhand volley toward Medvedev's backhand-side direction. Extra8not spatially decoded here. |
| 4 | Medvedev | `b3` | Backhand toward Djokovic's backhand-side direction. No depth recorded. |
| 5 | Djokovic | `z29*` | Backhand volley winner down the middle. Extra9not spatially decoded here. |

This is five attempted strokes including serve. The serve is from the **ad half**, derived from normal-game serving alternation and its odd-numbered position in the game (the eighth point, source150). The [ITF serving rule17](https://www.itftennis.com/media/7221/2026-rules-of-tennis-english.pdf) starts each standard game from the right half and alternates. The same rule requires a successful serve to reach the diagonal service box, but gives no measured contact or bounce location for this match.

Honest emphasis: approach flag → two backhand volleys → winner, with recipient-relative direction labels. No exact player position, passing-shot gap, court coverage, volley height or ball path is recoverable.

## Exact point154: game point lost

Before: Djokovic serves at games5–6, pointsAD–40. Raw `1st`: **`c6f39b38b29f29f29b38b28f18f39b39b37y1n@`**; `2nd` empty. Notes: `Let on 4.` Medvedev wins.

`c` is the preceding let and does not count as the first active stroke or change turn order. The active serve is `6`: down theT. The note separately records a let on a wide serve; do not reclassify the activeTserve as wide. No route or landing coordinate for that let is available.

| Attempted stroke | Actor | Raw token | Verified shot and direction |
| --- | --- | --- | --- |
| 1 | Djokovic | `6` | First serve down theT. |
| 2 | Medvedev | `f39` | Forehand return toward Djokovic's backhand side; documented return-depth9. |
| 3 | Djokovic | `b38` | Backhand toward Medvedev's backhand side. |
| 4 | Medvedev | `b29` | Backhand toward Djokovic's middle. |
| 5 | Djokovic | `f29` | Forehand toward Medvedev's middle. |
| 6 | Medvedev | `f29` | Forehand toward Djokovic's middle. |
| 7 | Djokovic | `b38` | Backhand toward Medvedev's backhand side. |
| 8 | Medvedev | `b28` | Backhand toward Djokovic's middle. |
| 9 | Djokovic | `f18` | Forehand toward Medvedev's forehand side. |
| 10 | Medvedev | `f39` | Forehand toward Djokovic's backhand side. This is not the service return, so trailing9is not decoded as verified depth here. |
| 11 | Djokovic | `b39` | Backhand toward Medvedev's backhand side. |
| 12 | Medvedev | `b37` | Backhand toward Djokovic's backhand side. |
| 13 | Djokovic | `y1n@` | Backhand drop-shot attempt in forehand-side direction; net error, charted unforced. |

The final direction1is the attempted/projected direction. The net error supplies **no successful landing region on Medvedev's side**. Do not animate a ball landing short in the forehand service box, nor assign an exact collision point along the net. A generic net-error highlight and “backhand drop shot · net · unforced” is supported. Direction can remain a separate intended-direction label or projected baseline band clearly distinguished from an actual landing.

This is thirteen attempted strokes in the active point, including the failed final shot and excluding the let. Conventional rally counts that exclude the error can differ; avoid an unexplained “13-shot rally” statistic. It is again an ad-half serve, the twelfth game point.

## Exact point155: next serve wins

Before: Djokovic serves at games5–6, points40–40. Raw `1st`: **`4+f39w#`**; `2nd` empty. Djokovic wins.

| Attempted stroke | Actor | Raw token | Verified description |
| --- | --- | --- | --- |
| 1 | Djokovic | `4+` | First serve wide, followed forward. From the deuce half, the thirteenth game point. |
| 2 | Medvedev | `f39w#` | Forehand return in Djokovic-backhand-side direction; wide error, charted forced. Depth-like9must not become an in-court landing. |

There is **no Djokovic volley stroke** in this record. It is a serve-and-volley play won on the missed return. Do not invent a volley, a successful return bounce, an exact wide miss location or a run toward an assumed volley-contact point. The key honest visual distinction from150is “approach coded; return misses before another Djokovic shot.”

## Honest visual vocabulary

- **Serve:** highlight the legal serving half and diagonally opposite receiving service box; labelT/wide and approach separately. The broad half/box follows rules, not player-tracking coordinates. Do not put a launch dot at an invented location within that half.
- **Rally direction:** highlight a categorical recipient-relative baseline band, labelled “direction,” not “bounce.” Avoid connecting its centre to the next band with a line; that manufactures trajectories.
- **Actor:** use Djokovic/Medvedev labels or badges outside the court. A volley identifies a net-shot category; a groundstroke has a baseline default in the coding convention, but neither gives an XYplayer position. The workbook's net/baseline defaults (A192–A193) are categorical assumptions, not tracking observations.
- **Depth:** only the documented return-depth9on154's first return should gain a coarse depth label/region. Keep later numeric suffixes and155's error depth unresolved in the raw inspector.
- **Ending:** winner, net error or wide error can change a label/state. Error direction is attempted direction; missing the net is not a landing on the opposite side. There are no measured net-crossing points for the other shots either.
- **Sequence:** step through recorded shot order immediately. Any dwell duration is reader/presentation time, never match elapsed time. Keep raw token and actor visible so every displayed distinction is inspectable.

The court can make the verified categories legible. A spatially complete replay would require independent video annotation or tracking data and corresponding provenance; it cannot be reconstructed from these three codes alone.

## Independent implementation audit — 2026-10-23

Read-only review of `pressure-shots.js`, shot-view markup in `index.html` and the changed150/154/155narration in `demo.js`. No application files changed. **No material source/evidence defect found in the inspected implementation.**

A separate Node DOM-stub execution checked all **20tokens** (5+13+2), every alternating actor, every current direction strip and all region states against the independent decoding above. It confirmed:

- Djokovic's schematic end is left, facing right: his forehand-side category is lower and backhand-side upper. Medvedev's end is right, facing left: forehand upper and backhand lower. Direction strips sit outside the appropriate recipient baseline and are not plotted as bounces.
- The ad-side serves in150/154highlight the receiver's lower service box;155's deuce-side serve highlights the upper box. These orientations agree with a left-end server facing right. The captions distinguishTfromwide and explicitly identify serve-and-volley approach codes.
- Only154's first return (`f39`) receives a deep-return band, spanning the singles width independently of its direction strip. Later8/9digits in150/154produce no depth region.155's missed return produces no depth/landing region or fictional volley.
-154's final shot has intended direction1and a generic net-error region, with a charted unforced-error label.155's final return has intended direction3and a charted wide forced-error label. No exact miss/net-collision coordinate, flight path or player marker is generated. The SVG description identifies schematic ends and explains the categorical encoding.
- Selecting a rebuilt stroke button restores focus to its replacement; Home/End navigation and the end-jump control use the selected stroke. Native previous/next buttons and pressed states are wired consistently. Captions and source fragments are live-announced. These are source/DOM-stub findings, not assistive-technology testing.
- A deliberately mismatched token/source record was hidden; another valid case remained usable. Selecting an unsupported game point also hides the shot view. The guard validates token concatenation, source server, exact pre-point score and empty second-serve cell; it is deliberately case-specific, not a general metadata/hash validator.

Audit artifact: ignored `reports/discovery/tactical-demo/pressure-source-audit.json`. Inspected `pressure-shots.js` SHA-256 is stored there with every verified token/actor. Browser layout, native focus behavior at button-disabled boundaries, color contrast, rendered legibility and audience interest remain outside this source audit.

Final narrow source recheck: **pass**. Each of the three cases rejects an incorrect pre-point score while leaving another valid case usable. Previous/Next retain their focus while enabled and transfer it to the selected stroke when the triggering control becomes disabled at the boundary; exercised both directions for all three cases with a DOM stub. All20tokens/actors remain unchanged. Controls and ending shortcut now precede the court in DOM order, with unique IDs. The155headline “No volley needed” agrees with the missed-return record. Refreshed source SHA-256: `84d93bb3fca38ab5de14002da961939ac042eefd758dcbd45490f15ca6df1e17`. This narrow recheck adds no browser/layout certification.
