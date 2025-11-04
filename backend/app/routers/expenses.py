from fastapi import APIRouter
from sqlmodel import Session, select
from typing import List
from ..models import Expense
from ..database import engine

router = APIRouter()

@router.post("/add", response_model=Expense)
def add_expense(exp: Expense):
    with Session(engine) as session:
        session.add(exp)
        session.commit()
        session.refresh(exp)
        return exp

@router.get("/list", response_model=List[Expense])
def list_expenses(user_id: int):
    with Session(engine) as session:
        items = session.exec(select(Expense).where(Expense.user_id == user_id)).all()
        return items
