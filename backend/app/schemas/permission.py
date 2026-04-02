"""Permission schemas"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str = Field(..., description="Permission name (e.g., 'reports.read')")
    resource: str = Field(..., description="Resource type (e.g., 'reports', 'users')")
    action: str = Field(..., description="Action type (e.g., 'read', 'write', 'delete')")
    description: Optional[str] = Field(default=None, description="Permission description")


class PermissionCreate(PermissionBase):
    """Schema for creating a permission"""
    is_system: Optional[bool] = Field(default=False, description="Whether this is a system permission")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "reports.validate",
                "resource": "reports",
                "action": "validate",
                "description": "Permission to validate reports",
                "is_system": False
            }
        }


class PermissionUpdate(BaseModel):
    """Schema for updating a permission"""
    name: Optional[str] = Field(default=None, description="Permission name")
    resource: Optional[str] = Field(default=None, description="Resource type")
    action: Optional[str] = Field(default=None, description="Action type")
    description: Optional[str] = Field(default=None, description="Permission description")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Updated permission description"
            }
        }


class PermissionResponse(PermissionBase):
    """Schema for permission response"""
    id: UUID = Field(..., description="Permission ID")
    is_system: bool = Field(..., description="Whether this is a system permission")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "name": "reports.validate",
                "resource": "reports",
                "action": "validate",
                "description": "Permission to validate reports",
                "is_system": False,
                "created_at": "2026-04-02T10:00:00Z",
                "updated_at": "2026-04-02T10:00:00Z"
            }
        }
