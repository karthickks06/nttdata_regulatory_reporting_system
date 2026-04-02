"""Authentication schemas"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., min_length=8, description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class Token(BaseModel):
    """Token response schema"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(default=None, description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: Optional[int] = Field(default=None, description="Token expiration time in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class TokenRefresh(BaseModel):
    """Token refresh request schema"""
    refresh_token: str = Field(..., description="Refresh token")

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
            }
        }


class TokenData(BaseModel):
    """Token payload schema"""
    user_id: UUID = Field(..., description="User ID from token")
    username: str = Field(..., description="Username from token")
    email: Optional[EmailStr] = Field(default=None, description="User email")
    roles: Optional[list[str]] = Field(default=None, description="User roles")
    permissions: Optional[list[str]] = Field(default=None, description="User permissions")


class RegisterRequest(BaseModel):
    """User registration request schema"""
    username: str = Field(..., min_length=3, max_length=100, description="Desired username")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(default=None, max_length=255, description="Full name")
    department: Optional[str] = Field(default=None, max_length=100, description="Department")
    job_title: Optional[str] = Field(default=None, max_length=100, description="Job title")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john.doe@company.com",
                "password": "SecureP@ssw0rd",
                "full_name": "John Doe",
                "department": "Compliance",
                "job_title": "Compliance Analyst"
            }
        }


class PasswordChangeRequest(BaseModel):
    """Password change request schema"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "OldP@ssw0rd",
                "new_password": "NewSecureP@ssw0rd"
            }
        }


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr = Field(..., description="User email address")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@company.com"
            }
        }


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "reset-token-here",
                "new_password": "NewSecureP@ssw0rd"
            }
        }
