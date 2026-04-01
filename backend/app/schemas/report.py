"""Report schemas"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class ReportBase(BaseModel):
    """Base report schema"""
    report_type: str
    title: str
    description: Optional[str] = None


class ReportCreate(ReportBase):
    """Schema for creating a report"""
    report_data: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = None


class ReportUpdate(BaseModel):
    """Schema for updating a report"""
    title: Optional[str] = None
    description: Optional[str] = None
    report_data: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = None


class ReportResponse(ReportBase):
    """Schema for report response"""
    id: int
    report_data: Optional[Dict[str, Any]]
    file_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportGenerationRequest(BaseModel):
    """Schema for report generation request"""
    report_type: str
    title: str
    data: Dict[str, Any]
    format: str = "json"  # json, csv, excel
    options: Optional[Dict[str, Any]] = None


class ReportGenerationResponse(BaseModel):
    """Schema for report generation response"""
    success: bool
    report_id: Optional[int] = None
    file_path: Optional[str] = None
    error: Optional[str] = None
