"""
Admin routes: view all users, view single user, delete/suspend user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List

from app.database import users_collection
from app.schemas import UserResponse, MessageResponse
from app.models import user_helper
from app.dependencies import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(admin: dict = Depends(get_current_admin)):
    """Get a list of all registered users (excluding admin)."""
    users = []
    cursor = users_collection.find({"role": "user"})
    async for user in cursor:
        users.append(user_helper(user))
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, admin: dict = Depends(get_current_admin)):
    """Get a single user's details by ID."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format",
        )

    user = await users_collection.find_one({"_id": ObjectId(user_id), "role": "user"})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user_helper(user)


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: str, admin: dict = Depends(get_current_admin)):
    """Delete a user by ID."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format",
        )

    result = await users_collection.delete_one({"_id": ObjectId(user_id), "role": "user"})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return MessageResponse(message="User deleted successfully")


@router.patch("/users/{user_id}/suspend", response_model=MessageResponse)
async def suspend_user(user_id: str, admin: dict = Depends(get_current_admin)):
    """Toggle suspend/activate a user account."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format",
        )

    user = await users_collection.find_one({"_id": ObjectId(user_id), "role": "user"})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_status = not user.get("is_active", True)
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": new_status}},
    )

    action = "activated" if new_status else "suspended"
    return MessageResponse(message=f"User {action} successfully")
