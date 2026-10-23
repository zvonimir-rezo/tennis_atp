"""Build the two public Margins studies as a portable, verified static release.

Run from any directory: python3 scripts/build_study_release.py
No dependency, model, server, network access or source-CSV copying is required.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'gui/margins-experiment'
OUTPUT = ROOT / 'reports/releases/margins-static'
ARCHIVE = OUTPUT.with_suffix('.zip')
FILES = [
    'index.html', 'style.css', 'court.js', 'evidence.js', 'records.js',
    'assets/InstrumentSerif-Regular.ttf', 'assets/InstrumentSerif-Italic.ttf',
    'assets/OFL-InstrumentSerif.txt', 'assets/grass-turf.webp',
    'assets/grass-turf.webp.json', 'assets/favicon.svg',
    'tactical-demo/index.html', 'tactical-demo/demo.css', 'tactical-demo/demo.js',
    'tactical-demo/data.js', 'tactical-demo/comparison.js',
    'tactical-demo/shot-sequence.js', 'tactical-demo/pressure-shots.js',
    'tactical-demo/player-portraits.js', 'tactical-demo/source-points.json',
    'tactical-demo/assets/djokovic-portrait.webp',
    'tactical-demo/assets/medvedev-portrait.webp',
    'tactical-demo/assets/djokovic-portrait-640.webp',
    'tactical-demo/assets/medvedev-portrait-640.webp',
    'tactical-demo/assets/djokovic-hitter.webp',
    'tactical-demo/assets/medvedev-hitter.webp',
    'tactical-demo/assets/portrait-provenance.json',
    'tactical-demo/assets/portrait-web-derivatives.json',
    'tactical-demo/assets/portrait-responsive-derivatives.json',
]
GENERATED = ['DEPLOY.md', 'CREDITS.md', '_headers', 'release-manifest.json']
ALLOWED = set(FILES + GENERATED)
FROZEN_HASH = 'eb6f8cf0b7c3766f92f70424d9ec870a79a325e06360b4cba67b5444e62b1b5e'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        self.urls.extend(attrs[k] for k in ('href', 'src') if attrs.get(k))
        self.urls.extend(part.strip().split()[0] for part in attrs.get('srcset', '').split(',') if part.strip())


def validate_references():
    parsed = {}
    for name in FILES:
        path = OUTPUT / name
        if path.suffix == '.html':
            parser = References()
            parser.feed(path.read_text())
            parsed[path.resolve()] = parser
    count = 0
    for name in FILES:
        path = OUTPUT / name
        if path.suffix == '.html':
            urls = parsed[path.resolve()].urls
        elif path.suffix == '.css':
            urls = re.findall(r'url\([\'\"]?([^\)\'\"]+)', path.read_text())
        else:
            continue
        for url in urls:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                continue
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path.resolve()
            if target.is_dir():
                target /= 'index.html'
            if not target.is_relative_to(OUTPUT.resolve()) or not target.is_file():
                raise ValueError(f'Broken or escaping local reference in {name}: {url}')
            if parts.fragment and target.suffix == '.html':
                parser = parsed.get(target.resolve())
                if parser and unquote(parts.fragment) not in parser.ids:
                    raise ValueError(f'Missing anchor in {name}: {url}')
            count += 1
    return count


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    extras = {p.relative_to(OUTPUT).as_posix() for p in OUTPUT.rglob('*') if p.is_file()} - ALLOWED
    if extras:
        raise ValueError(f'Release directory contains unexpected files; inspect before rebuilding: {sorted(extras)}')
    for name in FILES:
        source = SOURCE / name
        if not source.is_file() or not source.resolve().is_relative_to(SOURCE.resolve()):
            raise ValueError(f'Invalid allowlisted source: {name}')
        target = OUTPUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    if digest(OUTPUT / 'tactical-demo/source-points.json') != FROZEN_HASH:
        raise ValueError('Frozen tactical evidence changed; audit before release')
    (OUTPUT / 'DEPLOY.md').write_text('''# Margins static release

Publish the contents of this folder as static files. There is no build command,
backend, environment variable, account integration or API requirement.

- Wimbledon study: `/` (or `<mount>/` when hosted under a subdirectory).
- Two ways forward: `/tactical-demo/` (or `<mount>/tactical-demo/`).

Local preview from this directory:

    python3 -m http.server 8768 --bind 127.0.0.1

Open `http://127.0.0.1:8768/tactical-demo/`. File URLs also work.
Keep the directory hierarchy; do not use an SPA fallback or rewrite all paths to
one index. Serve HTML, JavaScript, CSS, JSON, SVG, WebP and TTF with their normal
MIME types. JSON is deliberately public, frozen charted match evidence.

`_headers` supplies revalidation, nosniff and referrer settings for hosts that
support that format. On another host, configure the same settings there. Do not
cache unfingerprinted HTML or scripts immutably. No canonical URL was invented;
set host-specific social/canonical URLs only after the destination is chosen.

Before publishing, preview both routes and the link between them, inspect the
source disclosures/download, and check keyboard, phone and reduced motion.
The release was verified locally; this file does not claim a public deployment.
Preserve the credits and license files when hosting or adapting the material.

The accompanying ZIP has these files at its root. The release manifest records
SHA-256 for every payload file; the ZIP's SHA-256 is supplied beside it.
''')
    (OUTPUT / 'CREDITS.md').write_text('''# Credits and source boundaries

Data: Jeff Sackmann / Tennis Abstract Match Charting Project. Both selected
matches were charted by Zindaras. Attribution and CC BY-NC-SA 4.0 links remain
visible in each study. Source: https://github.com/JeffSackmann/tennis_MatchChartingProject
License: https://creativecommons.org/licenses/by-nc-sa/4.0/

The original-format tactical JSON contains the 110 second-set records from the
2023 US Open men's final. Wimbledon records are embedded in records.js. The
studies are historical explanations, not pre-match models or tracking replays.

Instrument Serif: official Google Fonts distribution; OFL retained in assets/.
The turf and neutral portraits are generated editorial illustrations, not match
photographs, player reactions or source measurements. Generation prompts and
web-derivative provenance are retained as JSON assets. Original PNG working
files remain in the source project; web-ready derivatives are included here.
No local workstation paths or internal reports are included in this release.
''')
    (OUTPUT / '_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Cache-Control: public, max-age=0, must-revalidate
''')
    for path in OUTPUT.rglob('*'):
        if path.is_file() and path.suffix in {'.html', '.js', '.css', '.json', '.md'}:
            if '/Users/' in path.read_text() or 'file:///' in path.read_text():
                raise ValueError(f'Local path leaked into public release: {path.name}')
    references = validate_references()
    manifest = {
        'entrypoints': ['/', '/tactical-demo/'],
        'local_references_verified': references,
        'frozen_tactical_sha256': FROZEN_HASH,
        'files': [{'path': name, 'bytes': (OUTPUT / name).stat().st_size, 'sha256': digest(OUTPUT / name)}
                  for name in sorted(ALLOWED - {'release-manifest.json'})],
    }
    (OUTPUT / 'release-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(ALLOWED):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (OUTPUT / name).read_bytes())
    sha = digest(ARCHIVE)
    ARCHIVE.with_suffix('.zip.sha256').write_text(f'{sha}  {ARCHIVE.name}\n')
    print(json.dumps({'directory': str(OUTPUT), 'archive': str(ARCHIVE), 'files': len(ALLOWED),
                      'local_references_verified': references, 'zip_sha256': sha}, indent=2))


if __name__ == '__main__':
    main()
