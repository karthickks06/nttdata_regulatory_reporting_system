"""Authentication schemas"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload schema"""
    user_id: int
    username: str
