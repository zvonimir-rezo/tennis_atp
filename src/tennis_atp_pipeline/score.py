from __future__ import annotations

import re
from typing import Any

SET_RE = re.compile(r"^(\d+)-(\d+)")
END_TOKENS = {"RET", "W/O", "DEF", "ABD", "Default", "Walkover"}


def parse_score(score: Any) -> dict[str, Any]:
    text = "" if score is None else str(score).strip()
    sets: list[tuple[int, int]] = []
    for token in text.split():
        clean = token.strip()
        if clean.upper() in END_TOKENS:
            break
        match = SET_RE.match(clean)
        if match:
            sets.append((int(match.group(1)), int(match.group(2))))

    winner_sets = sum(1 for w_games, l_games in sets if w_games > l_games)
    loser_sets = sum(1 for w_games, l_games in sets if l_games > w_games)
    winner_games = sum(w_games for w_games, _ in sets)
    loser_games = sum(l_games for _, l_games in sets)
    first_set_winner_won = sets[0][0] > sets[0][1] if sets else None

    return {
        "sets_played": len(sets),
        "winner_sets_won": winner_sets,
        "loser_sets_won": loser_sets,
        "winner_games_won": winner_games,
        "loser_games_won": loser_games,
        "first_set_winner_won": first_set_winner_won,
        "has_score_detail": bool(sets),
    }
