# Simple focus scoring heuristic

def score_focus(payload: dict) -> float:
    duration = payload.get("duration_minutes") or 25
    breaks = payload.get("breaks") or 0
    # longer sessions up to 90 minutes help, breaks reduce score
    base = min(duration / 90.0, 1.0)
    penalty = min(breaks * 0.1, 0.9)
    score = (base * (1 - penalty)) * 100
    return round(score, 1)
