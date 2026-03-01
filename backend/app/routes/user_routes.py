"""
User routes: profile view and update.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
from bson import ObjectId

from app.database import users_collection
from app.schemas import UserProfileUpdate, UserResponse, MessageResponse
from app.models import user_helper
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/user", tags=["User"])


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get the current user's profile."""
    return user_helper(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update the current user's profile (name, phone, address)."""
    update_fields = {}

    if update_data.name is not None:
        update_fields["name"] = update_data.name
    if update_data.phone is not None:
        update_fields["phone"] = update_data.phone
    if update_data.address is not None:
        update_fields["address"] = update_data.address

    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    await users_collection.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$set": update_fields},
    )

    updated_user = await users_collection.find_one({"_id": ObjectId(current_user["id"])})
    return user_helper(updated_user)
