from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Environment variables
MONGO_URL = os.getenv("MONGO_URL", os.getenv("DATABASE_URL", "mongodb://localhost:27017"))
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "optimal_life")

# Global client reference
client: AsyncIOMotorClient | None = None

def get_db(app=None):
    """Return a motor database instance. If app is provided, prefer app.state.db."""
    if app is not None and hasattr(app.state, "db"):
        return app.state.db
    if client is None:
        raise RuntimeError("Mongo client not initialized")
    return client[MONGO_DB_NAME]

async def connect_to_mongo(app):
    global client
    client = AsyncIOMotorClient(MONGO_URL)
    app.state.db = client[MONGO_DB_NAME]

async def close_mongo(app):
    global client
    if client is not None:
        client.close()
        client = None

def init_db():
    # No-op for MongoDB; collections are created on first insert.
    return
