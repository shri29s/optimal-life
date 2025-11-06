from fastapi import APIRouter, Request
from typing import List
from ..models import Expense

router = APIRouter()


@router.post("/add", response_model=Expense)
async def add_expense(exp: Expense, request: Request):
    db = request.app.state.db
    doc = exp.dict(exclude_unset=True)
    doc.pop("id", None)
    result = await db["expenses"].insert_one(doc)
    exp.id = str(result.inserted_id)
    return exp


@router.get("/list", response_model=List[Expense])
async def list_expenses(user_id: str, request: Request):
    db = request.app.state.db
    cursor = db["expenses"].find({"user_id": user_id})
    items = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(Expense(**doc))
    return items
