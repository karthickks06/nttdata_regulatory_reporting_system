"""Requirement schemas"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RequirementBase(BaseModel):
    """Base requirement schema"""
    requirement_text: str
    section: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    is_mandatory: bool = True
    deadline: Optional[datetime] = None


class RequirementCreate(RequirementBase):
    """Schema for creating a requirement"""
    regulatory_update_id: int


class RequirementUpdate(BaseModel):
    """Schema for updating a requirement"""
    requirement_text: Optional[str] = None
    section: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    is_mandatory: Optional[bool] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None
    implementation_notes: Optional[str] = None


class RequirementResponse(RequirementBase):
    """Schema for requirement response"""
    id: int
    regulatory_update_id: int
    status: str
    implementation_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
