from fastapi import APIRouter
from sqlmodel import Session, select
from typing import List
from ..models import Habit
from ..database import engine

router = APIRouter()

@router.post("/add", response_model=Habit)
def add_habit(h: Habit):
    with Session(engine) as session:
        session.add(h)
        session.commit()
        session.refresh(h)
        return h

@router.get("/list", response_model=List[Habit])
def list_habits(user_id: int):
    with Session(engine) as session:
        items = session.exec(select(Habit).where(Habit.user_id == user_id)).all()
        return items
