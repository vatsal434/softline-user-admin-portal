"""
Authentication routes: signup and login.
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone

from app.database import users_collection
from app.schemas import UserSignup, UserLogin, TokenResponse
from app.auth import hash_password, verify_password, create_access_token
from app.models import user_helper

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup):
    """Register a new user account."""
    # Check if email already exists
    existing = await users_collection.find_one({"email": user_data.email.lower()})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    now = datetime.now(timezone.utc).isoformat()
    new_user = {
        "email": user_data.email.lower(),
        "password": hash_password(user_data.password),
        "role": "user",
        "name": user_data.name,
        "phone": "",
        "address": "",
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }

    result = await users_collection.insert_one(new_user)
    user_id = str(result.inserted_id)

    token = create_access_token({"user_id": user_id, "role": "user"})

    return TokenResponse(
        access_token=token,
        role="user",
        user_id=user_id,
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login for both users and admin."""
    user = await users_collection.find_one({"email": credentials.email.lower()})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been suspended. Contact admin.",
        )

    user_id = str(user["_id"])
    role = user.get("role", "user")

    token = create_access_token({"user_id": user_id, "role": role})

    return TokenResponse(
        access_token=token,
        role=role,
        user_id=user_id,
    )
