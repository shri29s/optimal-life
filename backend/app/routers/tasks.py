from fastapi import APIRouter, Request
from typing import List
from ..models import Task

router = APIRouter()


@router.post("/add", response_model=Task)
async def add_task(task: Task, request: Request):
    db = request.app.state.db
    task_doc = task.dict(exclude_unset=True)
    # Remove id if present
    task_doc.pop("id", None)
    result = await db["tasks"].insert_one(task_doc)
    task.id = str(result.inserted_id)
    return task


@router.get("/list", response_model=List[Task])
async def list_tasks(user_id: str, request: Request):
    db = request.app.state.db
    cursor = db["tasks"].find({"user_id": user_id})
    items = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(Task(**doc))
    return items
