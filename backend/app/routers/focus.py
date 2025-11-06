from fastapi import APIRouter, Request
from typing import List
from ..models import FocusSession

router = APIRouter()


@router.post("/add", response_model=FocusSession)
async def add_focus(session_payload: FocusSession, request: Request):
    db = request.app.state.db
    doc = session_payload.dict(exclude_unset=True)
    doc.pop("id", None)
    result = await db["focus_sessions"].insert_one(doc)
    session_payload.id = str(result.inserted_id)
    return session_payload


@router.get("/list", response_model=List[FocusSession])
async def list_focus(user_id: str, request: Request):
    db = request.app.state.db
    cursor = db["focus_sessions"].find({"user_id": user_id})
    items = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(FocusSession(**doc))
    return items
