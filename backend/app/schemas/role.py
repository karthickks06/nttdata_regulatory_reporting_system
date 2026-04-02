"""Role schemas"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """Base role schema"""
    name: str = Field(..., min_length=3, max_length=100, description="Role name (e.g., 'admin', 'analyst')")
    display_name: str = Field(..., max_length=255, description="Display name for the role")
    description: Optional[str] = Field(default=None, description="Role description")


class RoleCreate(RoleBase):
    """Schema for creating a role"""
    priority: Optional[int] = Field(default=0, description="Role priority (higher = more privileges)")
    permission_ids: Optional[List[UUID]] = Field(default=None, description="Permission IDs to assign")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "compliance_analyst",
                "display_name": "Compliance Analyst",
                "description": "Role for compliance analysts with read/write access",
                "priority": 5,
                "permission_ids": []
            }
        }


class RoleUpdate(BaseModel):
    """Schema for updating a role"""
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    display_name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    priority: Optional[int] = Field(default=None)
    permission_ids: Optional[List[UUID]] = Field(default=None, description="Permission IDs to assign")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Updated role description",
                "priority": 6
            }
        }


class RoleResponse(RoleBase):
    """Schema for role response"""
    id: UUID = Field(..., description="Role ID")
    is_system: bool = Field(..., description="Whether this is a system role")
    priority: int = Field(..., description="Role priority")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    permissions: Optional[List[str]] = Field(default=None, description="Permission names")
    user_count: Optional[int] = Field(default=None, description="Number of users with this role")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "name": "compliance_analyst",
                "display_name": "Compliance Analyst",
                "description": "Role for compliance analysts",
                "is_system": False,
                "priority": 5,
                "created_at": "2026-04-02T10:00:00Z",
                "updated_at": "2026-04-02T10:00:00Z",
                "permissions": ["reports.read", "reports.create", "requirements.read"],
                "user_count": 15
            }
        }
