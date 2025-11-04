# Simple keyword-based expense categorizer

CATEGORIES = {
    "food": ["restaurant","lunch","dinner","cafe","coffee","pizza","burger","uber eats","uber"],
    "rent": ["rent","apartment","lease"],
    "travel": ["train","uber","flight","plane","taxi","bus"],
    "entertainment": ["movie","netflix","concert","ticket"],
}

def categorize_expense(expense: dict) -> str:
    desc = (expense.get("description") or "").lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in desc:
                return cat
    return "other"
