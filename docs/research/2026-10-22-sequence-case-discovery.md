# A comeback without a break: Medvedev–Zverev, Australian Open 2024

Investigated 2026-10-22. Research candidate for Margins; no reusable system or product implementation. Match: 26 January 2024 semifinal, Daniil Medvedev over Alexander Zverev, 5–7 3–6 7–6(4) 7–6(5) 6–3. MCP identity: `20240126-M-Australian_Open-SF-Daniil_Medvedev-Alexander_Zverev`, charted by Edo. The [Australian Open match report](https://ausopen.com/articles/news/marathon-man-medvedev-third-ao-mens-final) corroborates the result and fourth-set escape.

## The discovery

Medvedev was broken **five times in his first eleven service games**. He then held **all sixteen remaining service games without facing another break point**. His service recovery was much clearer than the two tiebreak sets suggest.

Yet this recovery did not turn sets three and four into domination. Across their ordinary games, **Zverev still won more points, 64–63**. Medvedev's advantage was **14–9 in the two tiebreaks**, yielding two sets and an even match. At **5–4 Zverev in the fourth-set tiebreak, with Zverev serving the next two points**, Medvedev remained two points from defeat. He won both returns and then his own service point to force a fifth set.

The useful tension is a sustained recovery on serve coexisting with an extremely fragile route back into the match. The data supports a two-part account: Medvedev stopped giving Zverev break opportunities; he still needed two tiebreak wins before finally breaking again in the fifth. It does not establish a single psychological or causal turning point.

All numerical findings above are computed from the [MCP raw points](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-points-2020s.csv) by [sequence_case_probe.py](sequence_case_probe.py), with exact memberships and checks in ignored `reports/discovery/case-search-sequence/sequence-evidence.json`.

## Evidence and natural boundaries

Player order throughout is Medvedev / Zverev. Service-point rates include tiebreak service points; service games and break points exclude tiebreaks.

| Measure | Sets 1–2 | Sets 3–5 |
| --- | ---: | ---: |
| Point IDs | 1–127 | 128–326 |
| Medvedev service points won | 34/65 (52.3%) | 73/91 (80.2%) |
| Medvedev service games held | 6/11 | 16/16 |
| Break points faced by Medvedev | 10 | 0 |

The third set starts at point 128 on Zverev's serve. Medvedev's uninterrupted service-game run starts at point 132. The last break against him is point 127; the last break-point opportunities on his serve are points 126–127. Earlier break-point IDs are 12, 22, 60, 76, 101, 102, 104 and 106. These lists come from replayed score states, rather than an arbitrary definition of pressure.

| Recovery phase, sets 3–4 | Records | Medvedev points | Zverev points |
| --- | ---: | ---: | ---: |
| Ordinary games | 127 | 63 | 64 |
| Tiebreaks | 23 | 14 | 9 |
| All points | 150 | 77 | 73 |

The ordinary games are points 128–193 and 205–265; the breakers are 194–204 and 266–277. Each partition is complete and disjoint. All 24 ordinary service games in those two sets are holds. The later fifth-set breaks are retained, not concealed by the partition: Medvedev breaks at points 304 and 326.

Fourth-set close-up:

| Point | Pre-point score, Medvedev / Zverev | Server | Winner |
| --- | --- | --- | --- |
| 274 | 4–4 | Medvedev | Zverev |
| 275 | 4–5 | Zverev | Medvedev |
| 276 | 5–5 | Zverev | Medvedev |
| 277 | 6–5 | Medvedev | Medvedev |

The [Australian Open's player interview report](https://ausopen.com/articles/news/i-was-kind-just-hanging-on-zverev-flat-after-five-set-defeat) independently confirms Zverev's 5–4 lead with two serves and the mis-hit return at 5–5. Zverev also described diminished energy and loss of pressure on Medvedev's serve. Those are attributed player explanations; point counts cannot distinguish illness, fatigue, tactics and execution as causes.

## What a reader would discover

Opening question: **“He lost serve five times. How did he survive another three sets?”**

1. Show the first eleven service games, with five breaks and ten break-point opportunities visible.
2. Extend the same chronological record through the final sixteen holds. Let readers switch between Medvedev's service games, return games and tiebreaks. Keep the score visible so the service recovery can be seen before match-score parity.
3. Focus on sets three and four: twenty-four holds, 63–64 ordinary points, and two tiebreak wins. A comeback can be substantial without becoming comfortable.
4. Open the fourth-set breaker at 4–5 and step through points 275–277. This is the strongest objection to portraying the recovery as inevitable.

Bounded verdict: **Medvedev's service collapse ended after set two. His comeback remained vulnerable until two tiebreaks made it count.** Readers can substantiate both halves from the same record.

This proposal is a case brief, not a new UI or a requirement for the future engine. The timing/serve layers distinguish it from Wimbledon's concentration story, although both can use persistent point identity.

## Verification

Run from the repository root:

```sh
python3 docs/research/sequence_case_probe.py
```

The standard-library probe reads retained original public files, writes only ignored derived outputs, and:

- Checks 326 unique, contiguous point IDs and exact match identity.
- Independently generates all 326 pre-point set scores, game scores, point scores, servers and game indices from the winners. Every raw state agrees. Server-relative point labels are converted explicitly; tiebreak service alternation is checked.
- Recovers the five final set scores and 3–2 winner without reading the box-score result to advance the state.
- Checks per-set and total service/return counts, service points won, break points faced and saved against twelve MCP Overview rows.
- Checks the local ATP row `2024-580`, match `225`, for player identities, result, both service-point totals/wins, both service-game totals and break-point counts. All agree for the claims used here.
- Checks all displayed partitions and the fourth-set three-point escape against exact IDs. Records full-input and frozen-subset SHA-256 values in the output manifest.

The [MCP dictionary](https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/data_dictionary.txt) defines point order, scores, server and winner fields. Raw metadata has a human `8pm` start field; no elapsed-time claim is made. MCP Overview and raw points share source lineage and are not independent witnesses.

Known irrelevant disagreement: MCP Overview records thirteen Medvedev aces, while the local ATP row records fourteen. The case makes no ace-count or shot-classification claim; points, scores, serve outcomes and break-point counts used here agree. Preserve the disagreement rather than relabeling a point to force agreement. Attribution: Jeff Sackmann / Tennis Abstract Match Charting Project, charted by Edo, [CC BY-NC-SA 4.0](https://github.com/JeffSackmann/tennis_MatchChartingProject#license).

Independent review: the tactical researcher separately grouped raw `Gm#` records, used last-point winners for completed games, and detected break points from server-relative raw scores without importing this probe. It reproduced 34/65 and 6/11 holds with ten break points in sets 1–2; 73/91 and 16/16 holds with zero break points in sets 3–5; the 63–64 and 14–9 recovery partitions; and the servers/winners at points 275–277. No material discrepancy was found. It approved the descriptive verdict subject to retaining the late near-defeat as an objection.

## Why this candidate

The initial aggregate scan considered 973 best-of-five metadata rows from 2017–2025 and found set-level Overview rows for 972. That broad shortlist included nonstandard NextGen matches; only ordinary ATP main-draw candidates were selected for the five raw-series inspections. This is editorial search, not a representative statistical study or a claim that the pattern is unique.

- **Sinner–Medvedev AO2024 final:** dramatic service-rate change, but retained Overview has 282 points versus 283 unique raw records, with Medvedev service points 138 versus 139. Deferred rather than silently reconciled. The observation predates this case and is not itself a discovery about the tennis.
- **Nadal–Medvedev AO2022 final:** raw series has 371 points and agrees with aggregate service denominators, but the initial hook returned to the familiar third-set 0–40 escape. No stronger distinct finding was established in this pass.
- **Tsitsipas–Djokovic RG2021 final:** 311 raw points and matching aggregate service denominators; later service security is promising, but this semifinal offers a clearer coexistence of recovery and near-defeat.
- **Bublik–De Minaur RG2025 R64:** 258 raw points and matching aggregate service denominators; a runner-up for future investigation. Five-set recovery alone is not enough to publish a second case.

Unknown: whether expert fans find this exact layering surprising and whether the proposed comparison makes it easier to understand. Neither numerical verification nor a familiar match result establishes appeal. No causal model, win-probability estimate or invented shot position is involved.
