from fastapi import APIRouter
from typing import Dict

from ..ml.task_prioritizer import predict_priority
from ..ml.expense_categorizer import categorize_expense
from ..ml.focus_tracker import score_focus
from ..ml.habit_coach import habit_correlation

router = APIRouter()

@router.get("/insights", response_model=Dict)
def get_insights():
    # Prototype: return static example insights powered by small ML stubs.
    insights = {
        "next_tasks": [
            {"id": 1, "title": "Example Task A", "priority": 0.92},
            {"id": 2, "title": "Example Task B", "priority": 0.81},
        ],
        "expense_example_category": categorize_expense({"description": "Lunch at pizza place", "amount": 12.5}),
        "focus_example_score": score_focus({"duration_minutes": 50, "breaks": 1}),
        "habit_example_correlation": habit_correlation({"sleep_hours":7, "exercise_minutes":30, "caffeine_mg":50, "mood":7}),
    }
    return insights
