# Deploy the Margins studies

The release is a static website containing both linked studies. The tennis model/API is separate and is not included.

## Build

From the repository root, run:

```sh
python3 scripts/build_study_release.py
```

Outputs:

- `reports/releases/margins-static/` — publish this directory’s contents.
- `reports/releases/margins-static.zip` — the same files, with no extra containing directory.
- `reports/releases/margins-static.zip.sha256` — archive integrity hash.

The builder copies only named public assets, checks every local HTML/CSS reference, checks the frozen tactical source hash, rejects unexpected output files and workstation paths, and writes a size/hash manifest. Rebuilding identical inputs produces the same ZIP. It uses only Python’s standard library and does not access the network.

## Preview the release

```sh
python3 -m http.server 8768 --bind 127.0.0.1 --directory reports/releases/margins-static
```

Open `http://127.0.0.1:8768/tactical-demo/`. The Wimbledon study is at `/`. If port8768 is already serving the verified release preview, use that running preview instead.

## Hosting settings

Use a static-file host. Publish the directory contents directly; no build command, API, environment variable, database or account integration is needed by the site. Preserve the complete directory hierarchy so the tactical study’s links to its sibling and shared fonts work. Relative paths also support deployment under a subdirectory.

Keep ordinary directory-index routing. Do not add an SPA rewrite to the tactical index. Serve HTML, JS, CSS, JSON, SVG, WebP and TTF with their normal MIME types. The JSON subset is intentionally public historical evidence.

The included `_headers` config is usable on hosts that recognize that format. Otherwise configure its three settings in the host: `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Cache-Control: public, max-age=0, must-revalidate`. Do not mark unfingerprinted HTML/scripts immutable. No canonical URL was invented; add host-specific URLs once a destination exists.

Preserve source attribution, CC BY-NC-SA4.0 links, font OFL, and asset provenance. Their copies and source boundaries are included in CREDITS.md. Working PNGs, local provenance paths, debugging/verification tools, predictor/model files and upstream CSVs are excluded.

## Release check

After the host has a candidate URL, check both routes, sibling navigation, a service-scope comparison, a source-record download and pressure-shot selection on desktop and phone. Verify the host applies MIME and cache settings. The package has been exercised locally at root and subdirectory URLs with native keyboard, emulated touch and reduced motion; that does not establish a public deployment or physical-device coverage.

No host, domain or paid service has been configured by this task. Publishing remains a separate action after choosing its destination.
