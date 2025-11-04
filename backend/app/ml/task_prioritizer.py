# Simple rule-based prioritizer placeholder

def predict_priority(task: dict) -> float:
    """Compute a priority score (0-1) from fields in task dict.
    Expects keys: importance (0-10), deadline (optional), energy (0-10), time_estimate (minutes)
    """
    importance = task.get("importance") or 5
    energy = task.get("energy") or 5
    time_est = task.get("time_estimate") or 30
    # simplistic scoring
    score = (importance * 0.6 + (10 - energy) * 0.2 + (30 / (time_est + 1)) * 0.2) / 10
    return max(0.0, min(1.0, round(score, 3)))
