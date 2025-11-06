from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase # Import the type hint for the database object
from fastapi import Request
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# --- Configuration ---
# Fallback to local MongoDB if environment variable is not set
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "neuroplan_db")

# Global client reference
client: AsyncIOMotorClient | None = None

# --- Lifecycle Functions ---

async def connect_to_mongo(app: Request):
    """Initializes and connects the MongoDB client."""
    global client
    print(f"Connecting to MongoDB at {MONGO_URL}")
    client = AsyncIOMotorClient(MONGO_URL)
    # Store the database instance in the app state for easy access
    app.state.db = client[MONGO_DB_NAME]
    print("MongoDB connection initialized.")

async def close_mongo(app: Request):
    """Closes the MongoDB client connection."""
    global client
    if client is not None:
        client.close()
        client = None
        print("MongoDB connection closed.")

def init_db():
    # No-op for MongoDB; collections are created on first insert.
    pass

# --- Dependency Injection ---

async def get_db(request: Request) -> AsyncIOMotorDatabase:
    """Dependency function to yield the MongoDB database object."""
    # Assumes connect_to_mongo has run and stored the database in app.state
    yield request.app.state.db


# Backwards compatibility: some modules import get_db_dependency
# Provide an alias so imports keep working.
get_db_dependency = get_db