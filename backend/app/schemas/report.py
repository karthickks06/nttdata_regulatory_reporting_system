"""Report schemas"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.report import ReportType, ReportStatus, ReportFormat


class ReportBase(BaseModel):
    """Base report schema"""
    report_name: str = Field(..., max_length=255, description="Report name")
    report_type: ReportType = Field(..., description="Type of report")
    report_format: ReportFormat = Field(default=ReportFormat.PDF, description="Report format")
    description: Optional[str] = Field(default=None, description="Report description")


class ReportCreate(ReportBase):
    """Schema for creating a report"""
    reporting_period_start: Optional[datetime] = Field(default=None, description="Reporting period start")
    reporting_period_end: Optional[datetime] = Field(default=None, description="Reporting period end")
    submission_deadline: Optional[datetime] = Field(default=None, description="Submission deadline")
    report_data: Optional[Dict[str, Any]] = Field(default=None, description="Report data")
    tags: Optional[List[str]] = Field(default=[], description="Tags")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "report_name": "Q1 2024 MiFID II Transaction Report",
                "report_type": "compliance",
                "report_format": "pdf",
                "description": "Quarterly transaction reporting",
                "reporting_period_start": "2024-01-01T00:00:00Z",
                "reporting_period_end": "2024-03-31T23:59:59Z",
                "submission_deadline": "2024-04-15T23:59:59Z",
                "tags": ["mifid", "quarterly"]
            }
        }


class ReportUpdate(BaseModel):
    """Schema for updating a report"""
    report_name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    status: Optional[ReportStatus] = Field(default=None)
    report_data: Optional[Dict[str, Any]] = Field(default=None)
    validation_results: Optional[List[Dict[str, Any]]] = Field(default=None)
    anomalies_detected: Optional[List[Dict[str, Any]]] = Field(default=None)
    quality_score: Optional[str] = Field(default=None)
    submission_reference: Optional[str] = Field(default=None, max_length=255)
    submission_confirmation: Optional[str] = Field(default=None, max_length=255)
    approval_notes: Optional[str] = Field(default=None)
    rejection_reason: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "approved",
                "quality_score": "98.5",
                "approval_notes": "Approved for submission"
            }
        }


class ReportResponse(ReportBase):
    """Schema for report response"""
    id: UUID = Field(..., description="Report ID")
    file_name: Optional[str] = Field(default=None, description="File name")
    file_path: Optional[str] = Field(default=None, description="File path")
    file_size: Optional[str] = Field(default=None, description="File size in bytes")
    file_hash: Optional[str] = Field(default=None, description="File hash")
    status: ReportStatus = Field(..., description="Report status")
    reporting_period_start: Optional[datetime] = Field(default=None, description="Period start")
    reporting_period_end: Optional[datetime] = Field(default=None, description="Period end")
    submission_deadline: Optional[datetime] = Field(default=None, description="Submission deadline")
    submission_reference: Optional[str] = Field(default=None, description="Submission reference")
    submission_confirmation: Optional[str] = Field(default=None, description="Confirmation number")
    submitted_at: Optional[datetime] = Field(default=None, description="Submission timestamp")
    report_data: Optional[Dict[str, Any]] = Field(default=None, description="Report data")
    validation_results: List[Dict[str, Any]] = Field(default=[], description="Validation results")
    anomalies_detected: List[Dict[str, Any]] = Field(default=[], description="Detected anomalies")
    quality_score: Optional[str] = Field(default=None, description="Quality score")
    approved_by: Optional[UUID] = Field(default=None, description="Approver user ID")
    approved_at: Optional[datetime] = Field(default=None, description="Approval timestamp")
    rejection_reason: Optional[str] = Field(default=None, description="Rejection reason")
    approval_notes: Optional[str] = Field(default=None, description="Approval notes")
    created_by: Optional[UUID] = Field(default=None, description="Creator user ID")
    reviewed_by: Optional[UUID] = Field(default=None, description="Reviewer user ID")
    tags: List[str] = Field(default=[], description="Tags")
    metadata: Dict[str, Any] = Field(default={}, description="Metadata")
    version: str = Field(default="1.0", description="Report version")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    generated_at: Optional[datetime] = Field(default=None, description="Generation timestamp")
    validated_at: Optional[datetime] = Field(default=None, description="Validation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "report_name": "Q1 2024 MiFID II Transaction Report",
                "report_type": "compliance",
                "report_format": "pdf",
                "status": "approved",
                "file_name": "mifid_q1_2024.pdf",
                "quality_score": "98.5",
                "reporting_period_start": "2024-01-01T00:00:00Z",
                "reporting_period_end": "2024-03-31T23:59:59Z",
                "submission_deadline": "2024-04-15T23:59:59Z",
                "created_at": "2024-04-01T10:00:00Z",
                "validated_at": "2024-04-02T14:00:00Z",
                "approved_at": "2024-04-03T09:00:00Z"
            }
        }


class ReportGenerationRequest(BaseModel):
    """Schema for report generation request"""
    report_name: str = Field(..., max_length=255, description="Report name")
    report_type: ReportType = Field(..., description="Report type")
    report_format: ReportFormat = Field(default=ReportFormat.PDF, description="Desired format")
    reporting_period_start: datetime = Field(..., description="Period start")
    reporting_period_end: datetime = Field(..., description="Period end")
    data_sources: Optional[List[str]] = Field(default=None, description="Data sources to include")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Data filters")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Generation options")

    class Config:
        json_schema_extra = {
            "example": {
                "report_name": "Daily Transaction Report",
                "report_type": "compliance",
                "report_format": "excel",
                "reporting_period_start": "2024-04-01T00:00:00Z",
                "reporting_period_end": "2024-04-01T23:59:59Z",
                "data_sources": ["transactions", "trades"],
                "filters": {"status": "completed"},
                "options": {"include_charts": True}
            }
        }


class ReportGenerationResponse(BaseModel):
    """Schema for report generation response"""
    success: bool = Field(..., description="Whether generation succeeded")
    report_id: Optional[UUID] = Field(default=None, description="Generated report ID")
    file_path: Optional[str] = Field(default=None, description="File path")
    file_size: Optional[str] = Field(default=None, description="File size")
    status: Optional[str] = Field(default=None, description="Current status")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    warnings: Optional[List[str]] = Field(default=[], description="Warning messages")
    generated_at: Optional[datetime] = Field(default=None, description="Generation timestamp")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "report_id": "uuid-here",
                "file_path": "/reports/daily_transaction_2024-04-01.pdf",
                "file_size": "2048576",
                "status": "completed",
                "warnings": [],
                "generated_at": "2024-04-02T10:00:00Z"
            }
        }


class ReportValidationRequest(BaseModel):
    """Schema for report validation request"""
    report_id: UUID = Field(..., description="Report ID to validate")
    validation_rules: Optional[List[str]] = Field(default=None, description="Specific rules to apply")
    strict_mode: bool = Field(default=False, description="Whether to use strict validation")

    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "uuid-here",
                "validation_rules": ["completeness", "accuracy", "consistency"],
                "strict_mode": True
            }
        }


class ReportValidationResponse(BaseModel):
    """Schema for report validation response"""
    report_id: UUID = Field(..., description="Report ID")
    valid: bool = Field(..., description="Whether report is valid")
    validation_results: List[Dict[str, Any]] = Field(..., description="Validation results")
    errors: List[str] = Field(default=[], description="Validation errors")
    warnings: List[str] = Field(default=[], description="Validation warnings")
    quality_score: Optional[float] = Field(default=None, description="Quality score (0-100)")
    anomalies_detected: List[Dict[str, Any]] = Field(default=[], description="Detected anomalies")
    validated_at: datetime = Field(..., description="Validation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "uuid-here",
                "valid": True,
                "validation_results": [
                    {"rule": "completeness", "passed": True},
                    {"rule": "accuracy", "passed": True}
                ],
                "errors": [],
                "warnings": ["Minor data quality issue in row 150"],
                "quality_score": 98.5,
                "anomalies_detected": [],
                "validated_at": "2024-04-02T14:00:00Z"
            }
        }
