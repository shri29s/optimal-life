from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db, connect_to_mongo, close_mongo
from .routers import auth, tasks, expenses, focus, habits, analytics

app = FastAPI(title="optimal-life API - Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Initialize MongoDB connection
    await connect_to_mongo(app)
    # Legacy compatibility: no-op for Mongo
    init_db()


@app.on_event("shutdown")
async def shutdown():
    await close_mongo(app)

app.include_router(auth.router, prefix="/auth", tags=["auth"]) 
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"]) 
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"]) 
app.include_router(focus.router, prefix="/focus", tags=["focus"]) 
app.include_router(habits.router, prefix="/habits", tags=["habits"]) 
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"]) 
