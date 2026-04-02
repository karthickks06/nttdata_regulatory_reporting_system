"""Regulatory update schemas"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from app.models.regulatory_update import RegulatorySource, ImpactLevel, ProcessingStatus


class RegulatoryUpdateBase(BaseModel):
    """Base regulatory update schema"""
    title: str = Field(..., max_length=500, description="Title of the regulatory update")
    source: RegulatorySource = Field(..., description="Regulatory source")
    reference_number: str = Field(..., max_length=100, description="Reference number")
    description: Optional[str] = Field(default=None, description="Description of the update")
    published_date: datetime = Field(..., description="Publication date")
    effective_date: Optional[datetime] = Field(default=None, description="Effective date")
    deadline_date: Optional[datetime] = Field(default=None, description="Deadline for compliance")
    url: Optional[str] = Field(default=None, description="Source URL")
    impact_level: Optional[ImpactLevel] = Field(default=ImpactLevel.MEDIUM, description="Impact level")


class RegulatoryUpdateCreate(RegulatoryUpdateBase):
    """Schema for creating a regulatory update"""
    file_path: Optional[str] = Field(default=None, max_length=500, description="Path to uploaded file")
    tags: Optional[List[str]] = Field(default=[], description="Tags for categorization")
    categories: Optional[List[str]] = Field(default=[], description="Categories")
    affected_systems: Optional[List[str]] = Field(default=[], description="Affected systems")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "MiFID II Reporting Requirements Update",
                "source": "esma",
                "reference_number": "ESMA/2024/001",
                "description": "Updates to transaction reporting requirements",
                "published_date": "2024-01-15T00:00:00Z",
                "effective_date": "2024-06-01T00:00:00Z",
                "deadline_date": "2024-05-31T23:59:59Z",
                "url": "https://www.esma.europa.eu/...",
                "impact_level": "high",
                "tags": ["mifid", "reporting"],
                "categories": ["transaction_reporting"],
                "affected_systems": ["trading_system", "reporting_system"]
            }
        }


class RegulatoryUpdateUpdate(BaseModel):
    """Schema for updating a regulatory update"""
    title: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None)
    effective_date: Optional[datetime] = Field(default=None)
    deadline_date: Optional[datetime] = Field(default=None)
    impact_level: Optional[ImpactLevel] = Field(default=None)
    is_processed: Optional[bool] = Field(default=None)
    processing_status: Optional[ProcessingStatus] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    categories: Optional[List[str]] = Field(default=None)
    affected_systems: Optional[List[str]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "impact_level": "critical",
                "processing_status": "completed",
                "is_processed": True
            }
        }


class RegulatoryUpdateResponse(RegulatoryUpdateBase):
    """Schema for regulatory update response"""
    id: UUID = Field(..., description="Regulatory update ID")
    file_path: Optional[str] = Field(default=None, description="Path to uploaded file")
    document_hash: Optional[str] = Field(default=None, description="Document hash for duplicate detection")
    is_processed: bool = Field(..., description="Whether the update has been processed")
    processing_status: ProcessingStatus = Field(..., description="Processing status")
    tags: List[str] = Field(default=[], description="Tags")
    categories: List[str] = Field(default=[], description="Categories")
    affected_systems: List[str] = Field(default=[], description="Affected systems")
    extracted_requirements_count: str = Field(default="0", description="Number of extracted requirements")
    uploaded_by: Optional[UUID] = Field(default=None, description="User who uploaded")
    processed_by: Optional[UUID] = Field(default=None, description="User who processed")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    processed_at: Optional[datetime] = Field(default=None, description="Processing completion timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "title": "MiFID II Reporting Requirements Update",
                "source": "esma",
                "reference_number": "ESMA/2024/001",
                "description": "Updates to transaction reporting requirements",
                "published_date": "2024-01-15T00:00:00Z",
                "effective_date": "2024-06-01T00:00:00Z",
                "deadline_date": "2024-05-31T23:59:59Z",
                "url": "https://www.esma.europa.eu/...",
                "impact_level": "high",
                "file_path": "/uploads/ESMA_2024_001.pdf",
                "document_hash": "sha256hash",
                "is_processed": True,
                "processing_status": "completed",
                "tags": ["mifid", "reporting"],
                "categories": ["transaction_reporting"],
                "affected_systems": ["trading_system"],
                "extracted_requirements_count": "15",
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T12:00:00Z",
                "processed_at": "2024-01-15T12:00:00Z"
            }
        }
