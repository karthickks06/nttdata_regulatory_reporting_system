"""Requirement schemas"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.requirement import RequirementStatus, RequirementPriority, RequirementCategory


class RequirementBase(BaseModel):
    """Base requirement schema"""
    requirement_text: str = Field(..., description="Text of the requirement")
    section: Optional[str] = Field(default=None, max_length=100, description="Section reference")
    sub_section: Optional[str] = Field(default=None, max_length=100, description="Sub-section reference")
    category: Optional[RequirementCategory] = Field(default=RequirementCategory.OTHER, description="Requirement category")
    priority: Optional[RequirementPriority] = Field(default=RequirementPriority.MEDIUM, description="Priority level")
    is_mandatory: bool = Field(default=True, description="Whether the requirement is mandatory")
    deadline: Optional[datetime] = Field(default=None, description="Implementation deadline")


class RequirementCreate(RequirementBase):
    """Schema for creating a requirement"""
    regulatory_update_id: UUID = Field(..., description="ID of the regulatory update")
    requirement_id: Optional[str] = Field(default=None, max_length=100, description="External requirement ID")
    technical_approach: Optional[str] = Field(default=None, description="Technical implementation approach")
    affected_systems: Optional[List[str]] = Field(default=[], description="Affected systems")
    dependencies: Optional[List[str]] = Field(default=[], description="Requirement dependencies")

    class Config:
        json_schema_extra = {
            "example": {
                "regulatory_update_id": "uuid-here",
                "requirement_id": "REQ-001",
                "requirement_text": "All transactions must be reported within T+1",
                "section": "Article 26",
                "sub_section": "Paragraph 1",
                "category": "reporting",
                "priority": "high",
                "is_mandatory": True,
                "deadline": "2024-06-01T00:00:00Z",
                "technical_approach": "Implement automated reporting pipeline",
                "affected_systems": ["trading_system", "reporting_system"],
                "dependencies": ["REQ-002"]
            }
        }


class RequirementUpdate(BaseModel):
    """Schema for updating a requirement"""
    requirement_text: Optional[str] = Field(default=None)
    section: Optional[str] = Field(default=None, max_length=100)
    sub_section: Optional[str] = Field(default=None, max_length=100)
    category: Optional[RequirementCategory] = Field(default=None)
    priority: Optional[RequirementPriority] = Field(default=None)
    is_mandatory: Optional[bool] = Field(default=None)
    deadline: Optional[datetime] = Field(default=None)
    status: Optional[RequirementStatus] = Field(default=None)
    implementation_notes: Optional[str] = Field(default=None)
    technical_approach: Optional[str] = Field(default=None)
    affected_systems: Optional[List[str]] = Field(default=None)
    dependencies: Optional[List[str]] = Field(default=None)
    has_gap: Optional[bool] = Field(default=None)
    gap_description: Optional[str] = Field(default=None)
    gap_severity: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_progress",
                "implementation_notes": "Working on data mapping",
                "has_gap": True,
                "gap_description": "Missing field in source system",
                "gap_severity": "high"
            }
        }


class RequirementResponse(RequirementBase):
    """Schema for requirement response"""
    id: UUID = Field(..., description="Requirement ID")
    regulatory_update_id: UUID = Field(..., description="Regulatory update ID")
    requirement_id: Optional[str] = Field(default=None, description="External requirement ID")
    status: RequirementStatus = Field(..., description="Current status")
    implementation_notes: Optional[str] = Field(default=None, description="Implementation notes")
    technical_approach: Optional[str] = Field(default=None, description="Technical approach")
    affected_systems: List[str] = Field(default=[], description="Affected systems")
    dependencies: List[str] = Field(default=[], description="Dependencies")
    has_gap: bool = Field(default=False, description="Whether there is a gap")
    gap_description: Optional[str] = Field(default=None, description="Gap description")
    gap_severity: Optional[str] = Field(default=None, description="Gap severity")
    assigned_to: Optional[UUID] = Field(default=None, description="Assigned user ID")
    approved_by: Optional[UUID] = Field(default=None, description="Approver user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "regulatory_update_id": "uuid-here",
                "requirement_id": "REQ-001",
                "requirement_text": "All transactions must be reported within T+1",
                "section": "Article 26",
                "sub_section": "Paragraph 1",
                "category": "reporting",
                "priority": "high",
                "is_mandatory": True,
                "deadline": "2024-06-01T00:00:00Z",
                "status": "in_progress",
                "implementation_notes": "Working on data mapping",
                "technical_approach": "Automated pipeline",
                "affected_systems": ["trading_system"],
                "dependencies": ["REQ-002"],
                "has_gap": False,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-20T15:30:00Z"
            }
        }
