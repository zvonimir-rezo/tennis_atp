"""Reproduce a bounded tactical discovery from frozen public MCP records.

Run from repo root: python3 docs/research/tactical_case_probe.py
Uses existing downloaded snapshots; never changes upstream CSVs. Standard library only.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

KEY = "20230910-M-US_Open-F-Novak_Djokovic-Daniil_Medvedev"
BASE = "https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/"
SHOT_CODES = "fbrsvzopuy lmhijktq".replace(" ", "")
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=Path("/private/tmp/atp-discovery-external"))
parser.add_argument("--out", type=Path, default=Path("reports/discovery/case-search-tactical"))
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(name):
    with (args.source / name).open(encoding="utf-8-sig", newline="") as handle:
        return [r for r in csv.DictReader(handle) if r["match_id"] == KEY]


rows = sorted(extract("charting-m-points-2020s.csv"), key=lambda r: int(r["Pt"]))
assert [int(r["Pt"]) for r in rows] == list(range(1, 216))
meta = extract("charting-m-matches.csv")
assert len(meta) == 1
overview = extract("charting-m-stats-Overview.csv")
shot_types = extract("charting-m-stats-ShotTypes.csv")
(args.out / "usopen2023-final-points.json").write_text(json.dumps(rows, indent=2) + "\n")
(args.out / "usopen2023-source-tables.json").write_text(json.dumps({"metadata": meta, "overview": overview, "shot_types": shot_types}, indent=2) + "\n")

# Independent tennis-score replay: source Pts is server / returner order.
sets, games, points = [0, 0], [0, 0], [0, 0]
server, tb_first_server = 1, None
game_number = 1
finished_sets = []
labels = {0: "0", 1: "15", 2: "30", 3: "40"}
replayed = []
for row in rows:
    p, other = int(row["Svr"]) - 1, 2 - int(row["Svr"])
    is_tb = games == [6, 6]
    if is_tb:
        if tb_first_server is None:
            tb_first_server = server
        n = sum(points)
        expected_server = tb_first_server if n == 0 or ((n - 1) // 2) % 2 else 3 - tb_first_server
    else:
        expected_server = server
    assert int(row["Svr"]) == expected_server, row
    assert [int(row["Set1"]), int(row["Set2"])] == sets, row
    assert [int(row["Gm1"]), int(row["Gm2"])] == games, row
    assert int(row["Gm#"].split()[0]) == game_number, row
    if is_tb:
        expected_pts = f"{points[p]}-{points[other]}"
    elif points[p] >= 3 and points[other] >= 3:
        expected_pts = "40-40" if points[p] == points[other] else "AD-40" if points[p] > points[other] else "40-AD"
    else:
        expected_pts = f"{labels[points[p]]}-{labels[points[other]]}"
    assert row["Pts"] == expected_pts, (row, expected_pts)
    replayed.append({"id": int(row["Pt"]), "set": sum(sets) + 1, "server": p + 1, "winner": int(row["PtWinner"]), "tb": is_tb})
    winner = int(row["PtWinner"]) - 1
    points[winner] += 1
    target = 10 if is_tb and sum(sets) == 4 else 7 if is_tb else 4
    if points[winner] >= target and points[winner] - points[1 - winner] >= 2:
        games[winner] += 1
        points = [0, 0]
        game_number += 1
        if is_tb or (games[winner] >= 6 and games[winner] - games[1 - winner] >= 2):
            finished_sets.append(games.copy())
            sets[winner] += 1
            games = [0, 0]
        server = 3 - tb_first_server if is_tb else 3 - server
        tb_first_server = None
assert finished_sets == [[6, 3], [7, 6], [6, 3]]
assert sets == [3, 0]


def annotate(row, replay):
    # c marks a service let. It is not a return shot and cannot advance alternation.
    code = (row["2nd"] or row["1st"]).lstrip("c")
    shots = re.findall("[" + SHOT_CODES + "][^" + SHOT_CODES + "]*", code)
    player = int(row["Svr"])
    own = [shot for i, shot in enumerate(shots) if (i % 2 == 1) == (player == 1)]
    return {**replay, "code": code, "drops": [s for s in own if s[0] in "uy"], "snv": player == 1 and code[1:2] == "+", "raw": row}


points = [annotate(row, replay) for row, replay in zip(rows, replayed)]


def summary(points):
    return {"n": len(points), "djokovic_won": sum(p["winner"] == 1 for p in points), "ids": [p["id"] for p in points]}


groups = {}
for scope, subset in [("match", points), ("set2", [p for p in points if p["set"] == 2])]:
    serve = [p for p in subset if p["server"] == 1]
    drops = [p for p in subset if p["drops"]]
    sv = [p for p in serve if p["snv"]]
    serve_drops = [p for p in serve if p["drops"]]
    assert not ({p["id"] for p in sv} & {p["id"] for p in drops})
    groups[scope] = {"all": summary(subset), "own_serve": summary(serve), "serve_volley": summary(sv), "drop_points": summary(drops), "own_serve_drop_points": summary(serve_drops), "return_drop_points": summary([p for p in drops if p["server"] == 2]), "other_service": summary([p for p in serve if not p["snv"] and not p["drops"]])}

# Raw-derived totals agree with the independently stored aggregate ShotTypes table.
drop_total = next(r for r in shot_types if r["player"] == "Novak Djokovic" and r["row"] == "Dr")
assert len([shot for p in points for shot in p["drops"]]) == int(drop_total["shots"]) == 14
assert groups["match"]["drop_points"]["n"] == 14  # no repeated own drop shots within a point
assert groups["match"]["drop_points"]["djokovic_won"] == int(drop_total["shots_in_pts_won"]) == 4
for set_name in ["Total", "1", "2", "3"]:
    for player, name in [(1, "Novak Djokovic"), (2, "Daniil Medvedev")]:
        sample = [p for p in points if set_name == "Total" or p["set"] == int(set_name)]
        own_serve = [p for p in sample if p["server"] == player]
        ov = next(r for r in overview if r["player"] == name and r["set"] == set_name)
        assert len(own_serve) == int(ov["serve_pts"])
        assert sum(p["winner"] == player for p in own_serve) == int(ov["first_won"]) + int(ov["second_won"])

assert (groups["set2"]["serve_volley"]["n"], groups["set2"]["serve_volley"]["djokovic_won"]) == (11, 11)
assert (groups["set2"]["drop_points"]["n"], groups["set2"]["drop_points"]["djokovic_won"]) == (11, 3)
assert (groups["set2"]["own_serve_drop_points"]["n"], groups["set2"]["own_serve_drop_points"]["djokovic_won"]) == (5, 1)
assert (groups["set2"]["other_service"]["n"], groups["set2"]["other_service"]["djokovic_won"]) == (36, 25)
by_id = {p["id"]: p for p in points}
assert by_id[122]["raw"]["Gm1"] == "3" and by_id[122]["raw"]["Gm2"] == "4"
assert by_id[122]["raw"]["Pts"] == by_id[150]["raw"]["Pts"] == "40-AD"
assert by_id[150]["raw"]["Gm1"] == "5" and by_id[150]["raw"]["Gm2"] == "6"
assert all(by_id[p]["snv"] and by_id[p]["winner"] == 1 for p in [122, 147, 150, 153, 155])
assert all(by_id[p]["drops"] and by_id[p]["winner"] == 2 for p in [143, 154])

# Independent local ATP boxscore, without relying on date matching alone.
with Path("atp_matches_2023.csv").open(newline="") as handle:
    atp = [r for r in csv.DictReader(handle) if r["tourney_name"] == "Us Open" and r["round"] == "F" and r["winner_name"] == "Novak Djokovic" and r["loser_name"] == "Daniil Medvedev"]
assert len(atp) == 1
assert int(atp[0]["w_svpt"]) == 109 and int(atp[0]["l_svpt"]) == 106
assert int(atp[0]["w_1stWon"]) + int(atp[0]["w_2ndWon"]) == 75

result = {"match_id": KEY, "metadata": meta[0], "replayed_states": len(replayed), "final_sets": finished_sets, "groups": groups, "selected_point_records": [p for p in points if p["set"] == 2 and (p["snv"] or p["drops"])], "source_fingerprints": {name: {"url": BASE + name, "sha256": digest(args.source / name)} for name in ["charting-m-points-2020s.csv", "charting-m-matches.csv", "charting-m-stats-Overview.csv", "charting-m-stats-ShotTypes.csv"]}, "frozen_points_sha256": digest(args.out / "usopen2023-final-points.json"), "qualification": "Descriptive outcome partitions, not a causal treatment comparison. No physical coordinates. Whole-match MCP serve-volley count differs from official US Open reporting; selected second-set count agrees."}
(args.out / "tactical-evidence.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"match_id": KEY, "replayed_states": len(replayed), "groups": groups}, indent=2))
