from fastapi import APIRouter
from sqlmodel import Session, select
from typing import List
from ..models import FocusSession
from ..database import engine

router = APIRouter()

@router.post("/add", response_model=FocusSession)
def add_focus(session_payload: FocusSession):
    with Session(engine) as session:
        session.add(session_payload)
        session.commit()
        session.refresh(session_payload)
        return session_payload

@router.get("/list", response_model=List[FocusSession])
def list_focus(user_id: int):
    with Session(engine) as session:
        items = session.exec(select(FocusSession).where(FocusSession.user_id == user_id)).all()
        return items
