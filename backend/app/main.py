"""
FastAPI Application Entry Point.
- Mounts routes
- Seeds the single admin account on startup
- Serves static frontend files
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import connect_db, close_db, users_collection
from app.auth import hash_password
from app.routes import auth_routes, user_routes, admin_routes

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@portal.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")


async def seed_admin():
    """Create the single admin account if it doesn't exist."""
    existing = await users_collection.find_one({"role": "admin"})
    if not existing:
        now = datetime.now(timezone.utc).isoformat()
        admin_doc = {
            "email": ADMIN_EMAIL.lower(),
            "password": hash_password(ADMIN_PASSWORD),
            "role": "admin",
            "name": "System Admin",
            "phone": "",
            "address": "",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        await users_collection.insert_one(admin_doc)
        print(f"👑 Admin account created: {ADMIN_EMAIL}")
    else:
        print(f"👑 Admin account already exists: {existing['email']}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await connect_db()
    await seed_admin()
    yield
    await close_db()


app = FastAPI(
    title="User Management Portal",
    description="A full-stack user management system with admin panel",
    version="1.0.0",
    lifespan=lifespan,
)

# ──────────────── CORS ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────── API Routes ────────────────
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(admin_routes.router)

# ──────────────── Serve Frontend ────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend")
FRONTEND_DIR = os.path.abspath(FRONTEND_DIR)

if os.path.exists(FRONTEND_DIR):
    app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

    @app.get("/{page}.html")
    async def serve_page(page: str):
        file_path = os.path.join(FRONTEND_DIR, f"{page}.html")
        if os.path.exists(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))
