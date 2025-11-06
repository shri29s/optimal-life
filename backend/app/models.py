from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId

# Import pydantic_core components for v2 compatibility
from pydantic_core import core_schema as cs, core_schema

# Helper class to handle MongoDB's BSON ObjectId validation
# backend/app/models.py (Final PyObjectId Class)

# Helper class to handle MongoDB's BSON ObjectId validation
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.json_or_python_schema(
            # 1. Validation Logic
            python_schema=core_schema.with_info_plain_validator_function(
                cls.validate_py_object
            ),
            # 2. Input/Output Type
            json_schema=core_schema.str_schema(),
            
            # 3. Serialization Logic (Minimal, Correct Pydantic v2 Call)
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate_py_object(cls, value: ObjectId | str, handler):
        """Custom validation logic that runs before Pydantic model validation."""
        if isinstance(value, ObjectId):
            return value
        if isinstance(value, str):
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid objectid format")
            return ObjectId(value)
        
        return handler(value)

    # Simplified __get_pydantic_json_schema__ for schema generation
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema=None, handler=None):
        return cls.__get_pydantic_core_schema__(cls, handler)

# --- Core Data Models ---

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Task(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    importance: Optional[int] = None
    energy: Optional[int] = None
    time_estimate: Optional[int] = None
    priority_score: Optional[float] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class Expense(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    description: str
    amount: float
    category: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class FocusSession(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    start_time: datetime
    duration_minutes: int
    breaks: Optional[int] = 0
    focus_score: Optional[float] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class Habit(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    caffeine_mg: Optional[int] = None
    mood: Optional[int] = None
    correlation: Optional[float] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True