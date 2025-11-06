# Simple habit -> focus correlation heuristic

def habit_correlation(habit: dict) -> dict:
    sleep = habit.get("sleep_hours") or 7 
    exercise = habit.get("exercise_minutes") or 0
    caffeine = habit.get("caffeine_mg") or 0
    mood = habit.get("mood") or 5

    # crude correlation estimate: sleep + (exercise/60) - (caffeine/100)
    impact = (sleep - 7) * 0.1 + (exercise / 60.0) * 0.2 - (caffeine / 100.0) * 0.1
    estimated_focus_change_pct = round(impact * 100, 1)
    return {"estimated_focus_change_pct": estimated_focus_change_pct, "mood": mood}
