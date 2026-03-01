"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ──────────────── Auth Schemas ────────────────

class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str


# ──────────────── User Schemas ────────────────

class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=300)


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    name: str
    phone: str
    address: str
    is_active: bool
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    message: str
