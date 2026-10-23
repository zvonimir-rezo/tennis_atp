"""Reproduce the bounded AO2024 semifinal case; no app/model/data mutation.

python3 docs/research/sequence_case_probe.py

Reads the retained public MCP source in /private/tmp/atp-discovery-external.
Only generated outputs under ignored reports/discovery/case-search-sequence change.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path

MATCH = "20240126-M-Australian_Open-SF-Daniil_Medvedev-Alexander_Zverev"
SOURCE_URL = ("https://raw.githubusercontent.com/JeffSackmann/"
              "tennis_MatchChartingProject/master/charting-m-points-2020s.csv")


def load_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def score_labels(points):
    if min(points) >= 3:
        return ["40", "40"] if points[0] == points[1] else [
            "AD" if points[i] > points[1 - i] else "40" for i in range(2)]
    return [["0", "15", "30", "40"][p] for p in points]


def replay(rows):
    """Generate score/server from winners alone, checking every raw pre-point row.

    Specific scoring for this best-of-five AO2024 match: 7-point breakers in
    sets 1–4, 10-point breaker at 6–6 in set five. No fifth-set breaker occurs.
    """
    sets, games, points = [0, 0], [0, 0], [0, 0]
    server, first_server, game_start = 0, 0, 1
    completed_games, completed_sets, enriched = [], [], []
    game_bp = []
    for raw in rows:
        pid = int(raw["Pt"])
        assert max(sets) < 3, (pid, "point after match end")
        is_tb = games == [6, 6]
        if is_tb:
            server = first_server ^ (((sum(points) + 1) // 2) % 2)
            expected_score = [str(points[server]), str(points[1 - server])]
        else:
            expected = score_labels(points)
            expected_score = [expected[server], expected[1 - server]]
        assert [int(raw["Set1"]), int(raw["Set2"])] == sets, (pid, "sets")
        assert [int(raw["Gm1"]), int(raw["Gm2"])] == games, (pid, "games")
        assert int(raw["Svr"]) == server + 1, (pid, "server")
        assert raw["Pts"].split("-") == expected_score, (pid, "points", raw["Pts"], expected_score)
        assert int(raw["Gm#"].split()[0]) == len(completed_games) + 1, (pid, "game index")
        winner = int(raw["PtWinner"]) - 1
        bp = not is_tb and points[1 - server] >= 3 and points[1 - server] > points[server]
        if bp:
            game_bp.append(pid)
        enriched.append({"id": pid, "set": sum(sets) + 1, "server": server + 1,
                         "winner": winner + 1, "tiebreak": is_tb, "break_point": bp,
                         "pre_points_player_order": points.copy(),
                         "pre_games_player_order": games.copy(),
                         "pre_sets_player_order": sets.copy()})
        points[winner] += 1
        target = (10 if sum(sets) == 4 else 7) if is_tb else 4
        if points[winner] >= target and points[winner] - points[1 - winner] >= 2:
            games[winner] += 1
            completed_games.append({"set": sum(sets) + 1, "server": first_server + 1,
                                    "winner": winner + 1, "tiebreak": is_tb,
                                    "first_point": game_start, "last_point": pid,
                                    "break_point_ids": game_bp.copy()})
            set_won = is_tb or games[winner] >= 6 and games[winner] - games[1 - winner] >= 2
            if set_won:
                completed_sets.append({"score": games.copy(), "tiebreak_points": points.copy() if is_tb else None,
                                       "last_point": pid})
                sets[winner] += 1
                games = [0, 0]
            points, game_bp, game_start = [0, 0], [], pid + 1
            first_server = 1 - first_server
            server = first_server
    assert sets == [3, 2] and points == [0, 0] and games == [0, 0], ("final", sets, games, points)
    assert [s["score"] for s in completed_sets] == [[5, 7], [3, 6], [7, 6], [7, 6], [6, 3]]
    return enriched, completed_games, completed_sets


def stats(rows, games):
    result = {"points": len(rows), "point_ids": [r["id"] for r in rows],
              "wins": [sum(r["winner"] == p for r in rows) for p in (1, 2)]}
    for player in (1, 2):
        service = [r for r in rows if r["server"] == player]
        regular_games = [g for g in games if g["server"] == player and not g["tiebreak"]]
        result[str(player)] = {"service_won": sum(r["winner"] == player for r in service),
                               "service_points": len(service), "service_games": len(regular_games),
                               "holds": sum(g["winner"] == player for g in regular_games),
                               "bp_faced": sum(r["break_point"] for r in service),
                               "bp_saved": sum(r["break_point"] and r["winner"] == player for r in service)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=Path("/private/tmp/atp-discovery-external"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    out = root / "reports/discovery/case-search-sequence"
    out.mkdir(parents=True, exist_ok=True)
    source = args.source_dir / "charting-m-points-2020s.csv"
    rows = sorted((r for r in load_csv(source) if r["match_id"] == MATCH), key=lambda r: int(r["Pt"]))
    assert [int(r["Pt"]) for r in rows] == list(range(1, 327))
    metadata = next(r for r in load_csv(args.source_dir / "charting-m-matches.csv") if r["match_id"] == MATCH)
    point_path = out / (MATCH + ".json")
    point_path.write_text(json.dumps(rows, indent=2) + "\n")
    points, games, sets = replay(rows)
    groups = {}
    for label, allowed, mode in [("first_two_sets", {1, 2}, None), ("last_three_sets", {3, 4, 5}, None),
                                  ("recovery_sets_all", {3, 4}, None),
                                  ("recovery_sets_regular", {3, 4}, False),
                                  ("recovery_sets_tiebreak", {3, 4}, True)]:
        selected = [r for r in points if r["set"] in allowed and (mode is None or r["tiebreak"] == mode)]
        selected_games = [g for g in games if g["set"] in allowed and (mode is None or g["tiebreak"] == mode)]
        groups[label] = stats(selected, selected_games)
    per_set = {str(s): stats([r for r in points if r["set"] == s], [g for g in games if g["set"] == s]) for s in range(1, 6)}
    all_stats = stats(points, games)
    overview = [r for r in load_csv(args.source_dir / "charting-m-stats-Overview.csv") if r["match_id"] == MATCH]
    checks = []
    for row in overview:
        player = "1" if row["player"] == metadata["Player 1"] else "2"
        observed = all_stats if row["set"] == "Total" else per_set[row["set"]]
        other = "2" if player == "1" else "1"
        expected = {"serve_pts": observed[player]["service_points"],
                    "return_pts": observed[other]["service_points"],
                    "return_pts_won": observed[other]["service_points"] - observed[other]["service_won"],
                    "bk_pts": observed[player]["bp_faced"], "bp_saved": observed[player]["bp_saved"]}
        for key, value in expected.items():
            assert int(row[key]) == value, (row["set"], player, key, row[key], value)
        assert int(row["first_won"]) + int(row["second_won"]) == observed[player]["service_won"]
        checks.append({"set": row["set"], "player": player, "fields_checked": list(expected) + ["first_won+second_won"]})
    local = [r for r in load_csv(root / "atp_matches_2024.csv")
             if r["tourney_id"] == "2024-580" and r["match_num"] == "225"]
    assert len(local) == 1
    local = local[0]
    assert local["winner_name"] == metadata["Player 1"] and local["loser_name"] == metadata["Player 2"]
    assert local["score"] == "5-7 3-6 7-6(4) 7-6(5) 6-3"
    for prefix, player in [("w", "1"), ("l", "2")]:
        for key, expected in [("svpt", all_stats[player]["service_points"]),
                              ("SvGms", all_stats[player]["service_games"]),
                              ("bpSaved", all_stats[player]["bp_saved"]),
                              ("bpFaced", all_stats[player]["bp_faced"])]:
            assert int(local[prefix + "_" + key]) == expected
        assert int(local[prefix + "_1stWon"]) + int(local[prefix + "_2ndWon"]) == all_stats[player]["service_won"]
    assert groups["first_two_sets"]["1"] == {"service_won": 34, "service_points": 65, "service_games": 11, "holds": 6, "bp_faced": 10, "bp_saved": 5}
    assert groups["last_three_sets"]["1"] == {"service_won": 73, "service_points": 91, "service_games": 16, "holds": 16, "bp_faced": 0, "bp_saved": 0}
    assert groups["recovery_sets_regular"]["wins"] == [63, 64]
    assert groups["recovery_sets_tiebreak"]["wins"] == [14, 9]
    assert points[274]["pre_points_player_order"] == [4, 5] and points[274]["server"] == 2
    assert [r["winner"] for r in points[274:277]] == [1, 1, 1]
    assert [r["id"] for r in points if r["server"] == 1 and r["break_point"]] == [12, 22, 60, 76, 101, 102, 104, 106, 126, 127]
    manifest = {"match_id": MATCH, "source_url": SOURCE_URL, "metadata": metadata,
                "inputs": {p.name: digest(p) for p in [source, args.source_dir / "charting-m-matches.csv",
                    args.source_dir / "charting-m-stats-Overview.csv", root / "atp_matches_2024.csv"]},
                "frozen_points_sha256": digest(point_path), "scoring_replay": "326/326 pre-point scores, servers, set/game states and game indices agree",
                "overview_checks": checks, "local_atp_checked": ["match identity", "result", "service points", "service points won", "service games", "bp faced", "bp saved"],
                "source_limits": ["MCP has 13 Medvedev aces; local ATP has 14. Aces/shot classifications are outside this case's claims.",
                    "Overview and points are related source products, not independent witnesses; local ATP result and service/BP totals provide a separate cross-check.",
                    "Selected retrospectively; no causal or psychological inference, uniqueness claim or population significance."],
                "groups": groups, "per_set": per_set, "games": games, "sets": sets,
                "fourth_set_tiebreak_final_three": points[274:277]}
    (out / "sequence-evidence.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"match": MATCH, "replay": manifest["scoring_replay"],
                      "first_two": groups["first_two_sets"]["1"], "last_three": groups["last_three_sets"]["1"],
                      "recovery_regular": groups["recovery_sets_regular"]["wins"],
                      "recovery_tiebreak": groups["recovery_sets_tiebreak"]["wins"],
                      "output": str(out / "sequence-evidence.json")}, indent=2))


if __name__ == "__main__":
    main()
