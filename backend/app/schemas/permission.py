"""Permission schemas"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str
    resource: str
    action: str
    description: Optional[str] = None


class PermissionResponse(PermissionBase):
    """Schema for permission response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
