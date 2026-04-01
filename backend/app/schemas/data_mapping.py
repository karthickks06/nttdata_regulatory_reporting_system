"""Data mapping schemas"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class DataMappingBase(BaseModel):
    """Base data mapping schema"""
    source_system: str
    source_field: str
    target_system: str
    target_field: str
    transformation_logic: Optional[str] = None
    is_active: bool = True


class DataMappingCreate(DataMappingBase):
    """Schema for creating a data mapping"""
    requirement_id: Optional[int] = None


class DataMappingUpdate(BaseModel):
    """Schema for updating a data mapping"""
    source_system: Optional[str] = None
    source_field: Optional[str] = None
    target_system: Optional[str] = None
    target_field: Optional[str] = None
    transformation_logic: Optional[str] = None
    is_active: Optional[bool] = None


class DataMappingResponse(DataMappingBase):
    """Schema for data mapping response"""
    id: int
    requirement_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
