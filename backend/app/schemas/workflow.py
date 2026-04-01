"""Workflow schemas"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class WorkflowBase(BaseModel):
    """Base workflow schema"""
    name: str
    workflow_type: str
    description: Optional[str] = None


class WorkflowCreate(WorkflowBase):
    """Schema for creating a workflow"""
    workflow_definition: Dict[str, Any]
    status: str = "pending"


class WorkflowUpdate(BaseModel):
    """Schema for updating a workflow"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    workflow_definition: Optional[Dict[str, Any]] = None


class WorkflowResponse(WorkflowBase):
    """Schema for workflow response"""
    id: int
    workflow_definition: Dict[str, Any]
    status: str
    result: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class WorkflowExecutionRequest(BaseModel):
    """Schema for workflow execution request"""
    workflow_id: int


class WorkflowExecutionResponse(BaseModel):
    """Schema for workflow execution response"""
    success: bool
    workflow_id: int
    status: str
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
