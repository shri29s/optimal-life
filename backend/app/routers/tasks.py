# In backend/app/routers/tasks.py

from fastapi import APIRouter, Depends
from typing import List
from ..models import Task # Import Task model from updated models.py
from ..ml.task_prioritizer import predict_priority 
from ..database import get_db # Import MongoDB dependency
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId # Useful for filtering by ID

router = APIRouter()

@router.post("/add", response_model=Task)
async def add_task(task: Task, db: AsyncIOMotorDatabase = Depends(get_db)):
    tasks_collection = db["tasks"] # Access the 'tasks' collection

    # Calculate priority score before saving
    priority = predict_priority({
        "importance": task.importance,
        "energy": task.energy,
        "time_estimate": task.time_estimate
    })
    task.priority_score = priority
    
    # Convert Pydantic model to dictionary for MongoDB insert
    task_dict = task.dict(exclude_none=True, by_alias=True)
    
    # Insert document (MongoDB syntax)
    result = await tasks_collection.insert_one(task_dict)
    
    # Retrieve the inserted document to get the full object back
    new_task_doc = await tasks_collection.find_one({"_id": result.inserted_id})
    
    # Return the Pydantic model representation
    return Task.parse_obj(new_task_doc) 


@router.get("/list", response_model=List[Task])
async def list_tasks(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    tasks_collection = db["tasks"]

    # Retrieve documents for the specific user ID (MongoDB syntax)
    # The user_id field in the Task document is a string
    cursor = tasks_collection.find({"user_id": user_id}) 
    
    # Convert all documents to a list
    task_list = await cursor.to_list(length=None)
    
    # Convert list of MongoDB documents to a list of Pydantic Task models
    return [Task.parse_obj(doc) for doc in task_list]