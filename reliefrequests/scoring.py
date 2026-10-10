"""Aegis priority scoring (from the project proposal).

Medical emergency +5 | No food/water +4 | More than 50 affected +3 | Children/elderly +2
A request with none of these is a normal request and scores 1.
Bands: 8+ Critical, 5-7 High, 3-4 Medium, 1-2 Low.
"""
WEIGHTS = {"medical": 5, "no_supplies": 4, "large_household": 3, "vulnerable": 2}
MAX_SCORE = sum(WEIGHTS.values())  # 14


def calculate_priority(*, medical=False, no_supplies=False, household_size=1, vulnerable=False):
    score = 0
    score += WEIGHTS["medical"] if medical else 0
    score += WEIGHTS["no_supplies"] if no_supplies else 0
    score += WEIGHTS["large_household"] if household_size > 50 else 0
    score += WEIGHTS["vulnerable"] if vulnerable else 0
    score = score or 1
    return score, band_for(score)


def band_for(score):
    if score >= 8:
        return "critical"
    if score >= 5:
        return "high"
    if score >= 3:
        return "medium"
    return "low"
