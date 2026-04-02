"""User schemas"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: Optional[str] = Field(default=None, max_length=255, description="Full name")
    department: Optional[str] = Field(default=None, max_length=100, description="Department")
    job_title: Optional[str] = Field(default=None, max_length=100, description="Job title")
    phone_number: Optional[str] = Field(default=None, max_length=20, description="Phone number")


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=8, description="Password")
    role_ids: Optional[List[UUID]] = Field(default=None, description="Role IDs to assign")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john.doe@company.com",
                "full_name": "John Doe",
                "department": "Compliance",
                "job_title": "Analyst",
                "password": "SecureP@ssw0rd",
                "role_ids": []
            }
        }


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    email: Optional[EmailStr] = Field(default=None)
    full_name: Optional[str] = Field(default=None, max_length=255)
    department: Optional[str] = Field(default=None, max_length=100)
    job_title: Optional[str] = Field(default=None, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    password: Optional[str] = Field(default=None, min_length=8)
    is_active: Optional[bool] = Field(default=None)
    role_ids: Optional[List[UUID]] = Field(default=None, description="Role IDs to assign")

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe Jr.",
                "job_title": "Senior Analyst"
            }
        }


class UserResponse(UserBase):
    """Schema for user response"""
    id: UUID = Field(..., description="User ID")
    is_active: bool = Field(..., description="Whether user is active")
    is_superuser: bool = Field(..., description="Whether user is superuser")
    is_verified: bool = Field(..., description="Whether user email is verified")
    avatar_url: Optional[str] = Field(default=None, description="Avatar URL")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login: Optional[datetime] = Field(default=None, description="Last login timestamp")
    roles: Optional[List[str]] = Field(default=None, description="User role names")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "username": "johndoe",
                "email": "john.doe@company.com",
                "full_name": "John Doe",
                "department": "Compliance",
                "job_title": "Analyst",
                "phone_number": "+1234567890",
                "is_active": True,
                "is_superuser": False,
                "is_verified": True,
                "created_at": "2026-04-02T10:00:00Z",
                "updated_at": "2026-04-02T10:00:00Z",
                "last_login": "2026-04-02T12:30:00Z",
                "roles": ["analyst", "viewer"]
            }
        }
