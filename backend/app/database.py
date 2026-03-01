"""
Database connection module using Motor (async MongoDB driver).
"""

import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load .env from the backend directory (parent of app/)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path, override=True)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "user_management_portal")

client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=10000)
database = client[DATABASE_NAME]

# Collections
users_collection = database["users"]


async def connect_db():
    """Verify MongoDB connection on startup."""
    try:
        await client.admin.command("ping")
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise e


async def close_db():
    """Close MongoDB connection on shutdown."""
    client.close()
    print("🔌 MongoDB connection closed.")
