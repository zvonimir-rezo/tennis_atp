from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EloConfig:
    initial_rating: float = 1500.0
    k_factor: float = 32.0
    surface_blend: float = 0.5


def expected_score(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + 10 ** (-(rating_a - rating_b) / 400.0))

def calculate_k_factor(
    matches_played: int, 
    tourney_level: str = "A",
    best_of: int = 3,
    sets_won: int = 2,
    sets_lost: int = 0
) -> float:
    # Base K factor scales with matches played, but shouldn't drop to 0
    # Standard practice uses an exponent (like 0.4) to keep K reasonable for veterans
    base_k = 250.0 / ((matches_played + 5.0) ** 0.4)
    
    # Tournament multiplier
    multipliers = {
        "G": 1.0,     # Grand Slams
        "F": 0.9,     # Tour Finals
        "M": 0.85,    # Masters 1000
        "A": 0.75,    # ATP 250/500
        "D": 0.75,    # Davis Cup
        "C": 0.5,     # Challenger
    }
    level_mult = multipliers.get(str(tourney_level).upper(), 0.75)
    
    # Margin of Victory (Sets) multiplier
    margin_mult = 1.0
    if best_of == 3:
        if sets_won == 2 and sets_lost == 0:
            margin_mult = 1.0
        elif sets_won == 2 and sets_lost == 1:
            margin_mult = 0.75
        else:
            margin_mult = 0.8  # Retirement or unusual score
    elif best_of == 5:
        if sets_won == 3 and sets_lost == 0:
            margin_mult = 1.0
        elif sets_won == 3 and sets_lost == 1:
            margin_mult = 0.85
        elif sets_won == 3 and sets_lost == 2:
            margin_mult = 0.70
        else:
            margin_mult = 0.85  # Retirement or unusual score
            
    return base_k * level_mult * margin_mult

def update_elo(
    rating_a: float, rating_b: float, actual_a: float, k_factor_a: float = 32.0, k_factor_b: float = 32.0
) -> tuple[float, float]:
    expected_a = expected_score(rating_a, rating_b)
    expected_b = 1.0 - expected_a
    actual_b = 1.0 - actual_a
    return (
        rating_a + k_factor_a * (actual_a - expected_a),
        rating_b + k_factor_b * (actual_b - expected_b),
    )
