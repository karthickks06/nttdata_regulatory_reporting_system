"""Regulatory update schemas"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.regulatory_update import RegulatorySource


class RegulatoryUpdateBase(BaseModel):
    """Base regulatory update schema"""
    title: str
    source: RegulatorySource
    reference_number: str
    description: Optional[str] = None
    published_date: datetime
    effective_date: Optional[datetime] = None
    url: Optional[str] = None
    impact_level: Optional[str] = None


class RegulatoryUpdateCreate(RegulatoryUpdateBase):
    """Schema for creating a regulatory update"""
    pass


class RegulatoryUpdateUpdate(BaseModel):
    """Schema for updating a regulatory update"""
    title: Optional[str] = None
    description: Optional[str] = None
    effective_date: Optional[datetime] = None
    impact_level: Optional[str] = None
    is_processed: Optional[bool] = None


class RegulatoryUpdateResponse(RegulatoryUpdateBase):
    """Schema for regulatory update response"""
    id: int
    file_path: Optional[str] = None
    is_processed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
