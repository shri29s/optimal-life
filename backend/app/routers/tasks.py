from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..models import Task, User
from ..database import engine

router = APIRouter()

@router.post("/add", response_model=Task)
def add_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@router.get("/list", response_model=List[Task])
def list_tasks(user_id: int):
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        return tasks
