"""Disposable, standard-library evidence probe; does not alter project data/models.

Run from the repository root. Use --fetch to retrieve the public MCP specimen.
"""
import argparse
import csv
import hashlib
import io
import itertools
import json
from pathlib import Path
import urllib.request

KEY = "20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic"
URL = ("https://raw.githubusercontent.com/JeffSackmann/"
       "tennis_MatchChartingProject/master/charting-m-points-2010s.csv")
OUT = Path("reports/discovery")
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--fetch", action="store_true")
args = parser.parse_args()
OUT.mkdir(parents=True, exist_ok=True)
specimen = OUT / "wimbledon2019-final-points.json"
if args.fetch:
    rows = []
    with urllib.request.urlopen(URL, timeout=35) as response:
        for row in csv.DictReader(io.TextIOWrapper(response, encoding="utf-8-sig")):
            if row["match_id"] == KEY:
                rows.append(row)
            elif rows:
                break
    rows.sort(key=lambda r: int(r["Pt"]))
    specimen.write_text(json.dumps(rows, indent=2))
rows = json.loads(specimen.read_text())
assert [int(r["Pt"]) for r in rows] == list(range(1, 423))
assert all(r["match_id"] == KEY for r in rows)

def counts(points):
    return {"federer": sum(r["PtWinner"] == "1" for r in points),
            "djokovic": sum(r["PtWinner"] == "2" for r in points)}

sets = []
for number, group in itertools.groupby(rows, key=lambda r: int(r["Set1"]) + int(r["Set2"]) + 1):
    points = list(group)
    games = [list(g) for _, g in itertools.groupby(points, key=lambda r: int(r["Gm#"]))]
    last = games[-1][0]
    tiebreak = games[-1] if last["Gm1"] == last["Gm2"] and int(last["Gm1"]) >= 6 else []
    sets.append({"set": number, "points": len(points), **counts(points),
                 "tiebreak": counts(tiebreak),
                 "first_point": int(points[0]["Pt"]), "last_point": int(points[-1]["Pt"])})
with open("atp_matches_2019.csv") as handle:
    local = next(r for r in csv.DictReader(handle)
                 if r["tourney_id"] == "2019-540" and r["match_num"] == "226")
djokovic = sum(int(local[k]) for k in ["w_1stWon", "w_2ndWon", "l_svpt"])
djokovic -= sum(int(local[k]) for k in ["l_1stWon", "l_2ndWon"])
federer = int(local["w_svpt"]) + int(local["l_svpt"]) - djokovic
assert counts(rows) == {"federer": federer, "djokovic": djokovic}
result = {"source": URL, "match_id": KEY,
          "attribution": "Jeff Sackmann / Tennis Abstract MCP; charted by Zindaras",
          "license": "CC BY-NC-SA 4.0", "subset_sha256": hashlib.sha256(specimen.read_bytes()).hexdigest(),
          "total": counts(rows), "sets": sets,
          "outside_second_set": counts([r for r in rows if int(r["Set1"]) + int(r["Set2"]) != 1]),
          "qualification": "Descriptive partition of recorded points, not a counterfactual match or a causal model."}
(OUT / "wimbledon2019-ledger.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
