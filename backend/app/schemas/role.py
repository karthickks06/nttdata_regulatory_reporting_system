"""Role schemas"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class RoleBase(BaseModel):
    """Base role schema"""
    name: str
    display_name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role"""
    pass


class RoleUpdate(BaseModel):
    """Schema for updating a role"""
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None


class RoleResponse(RoleBase):
    """Schema for role response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
