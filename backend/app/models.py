from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    importance: Optional[int] = None
    energy: Optional[int] = None
    time_estimate: Optional[int] = None
    priority_score: Optional[float] = None

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    description: str
    amount: float
    category: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)

class FocusSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    start_time: datetime
    duration_minutes: int
    breaks: Optional[int] = 0
    focus_score: Optional[float] = None

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    caffeine_mg: Optional[int] = None
    mood: Optional[int] = None
    correlation: Optional[float] = None
