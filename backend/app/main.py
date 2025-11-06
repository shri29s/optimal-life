from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORTANT: Import the new MongoDB lifecycle functions
from app.database import init_db, connect_to_mongo, close_mongo
from app.routers import auth, tasks, expenses, focus, habits, analytics
app = FastAPI(title="NeuroPlan API - MongoDB Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Attach MongoDB Lifecycle Events ---
@app.on_event("startup")
async def startup_event():
    # Initialize SQLite compatibility (No-op in database.py, but structure remains)
    init_db() 
    # Connect to MongoDB
    await connect_to_mongo(app) 

@app.on_event("shutdown")
async def shutdown_event():
    # Close MongoDB connection gracefully
    await close_mongo(app)

# --- Add Root Health Check Route ---
@app.get("/")
def read_root():
    return {"status": "ok", "app": "NeuroPlan API is running (MongoDB)"}

# --- Router Includes ---
app.include_router(auth.router, prefix="/auth", tags=["auth"]) 
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"]) 
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"]) 
app.include_router(focus.router, prefix="/focus", tags=["focus"]) 
app.include_router(habits.router, prefix="/habits", tags=["habits"]) 
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])