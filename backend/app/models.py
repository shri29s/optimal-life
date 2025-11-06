from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = {"from_attributes": True}


class Task(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    importance: Optional[int] = None
    energy: Optional[int] = None
    time_estimate: Optional[int] = None
    priority_score: Optional[float] = None

    class Config:
        pass


class Expense(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    description: str
    amount: float
    category: Optional[str] = None
    date: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        pass


class FocusSession(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    start_time: datetime
    duration_minutes: int
    breaks: Optional[int] = 0
    focus_score: Optional[float] = None

    class Config:
        pass


class Habit(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    caffeine_mg: Optional[int] = None
    mood: Optional[int] = None
    correlation: Optional[float] = None

    class Config:
        pass
