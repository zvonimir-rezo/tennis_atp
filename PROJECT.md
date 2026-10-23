# ATP project and Margins

This private repository preserves Jeff Sackmann's ATP dataset history and adds a Python modeling pipeline plus two self-contained interactive tennis studies. The original README documents the upstream dataset; this guide describes the added project.

## Margins website

Source: `gui/margins-experiment/`. The Wimbledon study is at its root; the Djokovic–Medvedev study is in `tactical-demo/`. Both use plain HTML, CSS, JavaScript and SVG, with bundled fonts and images. No Python inference server or database is required by these studies.

Build the portable release from the repository root:

```sh
python3 scripts/build_study_release.py
```

Publish the contents of `reports/releases/margins-static/`, or upload `reports/releases/margins-static.zip` through Cloudflare Pages Direct Upload. Preserve the directory hierarchy. Hosting instructions and smoke checks are in [docs/deploy_static_studies.md](docs/deploy_static_studies.md).

## Prediction prototype

Python 3.11 or newer is required by `pyproject.toml`. Core dependencies are pandas, NumPy, scikit-learn, PyArrow and joblib. The prototype interface runs with `python3 gui_server.py` at `http://127.0.0.1:8080/` after installing dependencies and generating the required model and player-state files. It is a local development server; public hosting needs separate preparation.

Generated models, processed data and reports are ignored by Git. A fresh clone does not include those artifacts. See [docs/bookmaking_pipeline.md](docs/bookmaking_pipeline.md) and the modules under `src/tennis_atp_pipeline/` for the modeling workflow. The older setup guide contains a stale port; use 8080 for the current server.

## Source history and credits

`origin` points to `zvonimir-rezo/tennis_atp`; `upstream` points to `JeffSackmann/tennis_atp`. This is a standalone private repository retaining the original history. The initial import leaves the previously missing upstream files in Git history and on GitHub; their local deletions were not committed.

Keep upstream dataset attribution, Match Charting Project attribution and CC BY-NC-SA 4.0 disclosures, bundled font licenses, and asset provenance. The release builder includes the relevant website credits in its output.
