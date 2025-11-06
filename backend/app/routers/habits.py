from fastapi import APIRouter, Request
from typing import List
from ..models import Habit

router = APIRouter()


@router.post("/add", response_model=Habit)
async def add_habit(h: Habit, request: Request):
    db = request.app.state.db
    doc = h.dict(exclude_unset=True)
    doc.pop("id", None)
    result = await db["habits"].insert_one(doc)
    h.id = str(result.inserted_id)
    return h


@router.get("/list", response_model=List[Habit])
async def list_habits(user_id: str, request: Request):
    db = request.app.state.db
    cursor = db["habits"].find({"user_id": user_id})
    items = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(Habit(**doc))
    return items
