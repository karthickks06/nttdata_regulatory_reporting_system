"""Workflow schemas"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.workflow import WorkflowType, WorkflowStatus, WorkflowPriority


class WorkflowBase(BaseModel):
    """Base workflow schema"""
    workflow_name: str = Field(..., max_length=255, description="Workflow name")
    workflow_type: WorkflowType = Field(..., description="Type of workflow")
    description: Optional[str] = Field(default=None, description="Workflow description")


class WorkflowCreate(WorkflowBase):
    """Schema for creating a workflow"""
    priority: Optional[int] = Field(default=WorkflowPriority.MEDIUM.value, ge=1, le=5, description="Priority (1=highest)")
    definition: Dict[str, Any] = Field(..., description="Workflow definition (steps, dependencies)")
    input_data: Dict[str, Any] = Field(..., description="Input data for workflow")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Shared context")
    variables: Optional[Dict[str, Any]] = Field(default={}, description="Workflow variables")
    timeout_seconds: Optional[str] = Field(default=None, description="Timeout in seconds")
    max_retries: Optional[int] = Field(default=3, description="Max retries on failure")
    requires_approval: Optional[str] = Field(default="false", description="Whether approval needed")
    tags: Optional[List[str]] = Field(default=[], description="Tags")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_name": "Regulatory Update Processing",
                "workflow_type": "regulatory_processing",
                "description": "Process new regulatory update",
                "priority": 2,
                "definition": {
                    "steps": [
                        {"name": "parse_document", "agent": "document_parser"},
                        {"name": "extract_requirements", "agent": "requirement_extractor"},
                        {"name": "create_mappings", "agent": "mapping_generator"}
                    ]
                },
                "input_data": {"update_id": "uuid-here"},
                "timeout_seconds": "3600",
                "tags": ["mifid", "urgent"]
            }
        }


class WorkflowUpdate(BaseModel):
    """Schema for updating a workflow"""
    workflow_name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    status: Optional[WorkflowStatus] = Field(default=None)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    state: Optional[Dict[str, Any]] = Field(default=None)
    context: Optional[Dict[str, Any]] = Field(default=None)
    variables: Optional[Dict[str, Any]] = Field(default=None)
    output_data: Optional[Dict[str, Any]] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "paused",
                "priority": 1
            }
        }


class WorkflowResponse(WorkflowBase):
    """Schema for workflow response"""
    id: UUID = Field(..., description="Workflow ID")
    status: WorkflowStatus = Field(..., description="Current status")
    priority: int = Field(..., description="Priority level")
    definition: Dict[str, Any] = Field(..., description="Workflow definition")
    state: Dict[str, Any] = Field(default={}, description="Current state")
    context: Dict[str, Any] = Field(default={}, description="Shared context")
    variables: Dict[str, Any] = Field(default={}, description="Variables")
    input_data: Optional[Dict[str, Any]] = Field(default=None, description="Input data")
    output_data: Optional[Dict[str, Any]] = Field(default=None, description="Output data")
    intermediate_results: Dict[str, Any] = Field(default={}, description="Intermediate results")
    error_message: Optional[str] = Field(default=None, description="Error message")
    error_traceback: Optional[str] = Field(default=None, description="Error traceback")
    error_step: Optional[str] = Field(default=None, description="Step where error occurred")
    retry_count: int = Field(default=0, description="Current retry count")
    max_retries: int = Field(default=3, description="Maximum retries")
    current_step: str = Field(default="0", description="Current step number")
    current_step_name: Optional[str] = Field(default=None, description="Current step name")
    total_steps: str = Field(default="0", description="Total steps")
    progress_percentage: int = Field(default=0, description="Progress percentage")
    step_history: List[Dict[str, Any]] = Field(default=[], description="Step history")
    estimated_duration_seconds: Optional[str] = Field(default=None, description="Estimated duration")
    actual_duration_seconds: Optional[str] = Field(default=None, description="Actual duration")
    timeout_seconds: Optional[str] = Field(default=None, description="Timeout")
    requires_approval: str = Field(default="false", description="Requires approval")
    approved_by: Optional[UUID] = Field(default=None, description="Approver user ID")
    approved_at: Optional[datetime] = Field(default=None, description="Approval timestamp")
    approval_notes: Optional[str] = Field(default=None, description="Approval notes")
    started_at: Optional[datetime] = Field(default=None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")
    paused_at: Optional[datetime] = Field(default=None, description="Pause timestamp")
    cancelled_at: Optional[datetime] = Field(default=None, description="Cancellation timestamp")
    created_by: Optional[UUID] = Field(default=None, description="Creator user ID")
    tags: List[str] = Field(default=[], description="Tags")
    metadata: Dict[str, Any] = Field(default={}, description="Metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "workflow_name": "Regulatory Update Processing",
                "workflow_type": "regulatory_processing",
                "status": "running",
                "priority": 2,
                "current_step": "2",
                "current_step_name": "extract_requirements",
                "total_steps": "5",
                "progress_percentage": 40,
                "retry_count": 0,
                "max_retries": 3,
                "started_at": "2024-04-02T10:00:00Z",
                "created_at": "2024-04-02T09:55:00Z",
                "updated_at": "2024-04-02T10:02:00Z"
            }
        }


class WorkflowExecutionRequest(BaseModel):
    """Schema for workflow execution request"""
    workflow_type: WorkflowType = Field(..., description="Type of workflow to execute")
    workflow_name: Optional[str] = Field(default=None, max_length=255, description="Optional workflow name")
    input_data: Dict[str, Any] = Field(..., description="Input data for workflow")
    priority: Optional[int] = Field(default=WorkflowPriority.MEDIUM.value, ge=1, le=5, description="Priority")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Execution options")
    timeout_seconds: Optional[int] = Field(default=None, description="Timeout")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_type": "regulatory_processing",
                "workflow_name": "Process ESMA Update",
                "input_data": {"update_id": "uuid-here"},
                "priority": 2,
                "options": {"auto_approve": False},
                "timeout_seconds": 3600
            }
        }


class WorkflowExecutionResponse(BaseModel):
    """Schema for workflow execution response"""
    workflow_id: UUID = Field(..., description="Workflow ID")
    workflow_type: str = Field(..., description="Workflow type")
    status: str = Field(..., description="Current status")
    current_step: str = Field(..., description="Current step")
    current_step_name: Optional[str] = Field(default=None, description="Current step name")
    progress_percentage: int = Field(..., description="Progress percentage")
    started_at: datetime = Field(..., description="Start timestamp")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion")
    error: Optional[str] = Field(default=None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "uuid-here",
                "workflow_type": "regulatory_processing",
                "status": "running",
                "current_step": "2",
                "current_step_name": "extract_requirements",
                "progress_percentage": 40,
                "started_at": "2024-04-02T10:00:00Z",
                "estimated_completion": "2024-04-02T11:00:00Z"
            }
        }


class WorkflowActionRequest(BaseModel):
    """Schema for workflow action request (pause, resume, cancel)"""
    workflow_id: UUID = Field(..., description="Workflow ID")
    action: str = Field(..., description="Action to perform (pause, resume, cancel, approve, reject)")
    reason: Optional[str] = Field(default=None, description="Reason for action")
    notes: Optional[str] = Field(default=None, description="Additional notes")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "uuid-here",
                "action": "pause",
                "reason": "Waiting for data validation",
                "notes": "Will resume after validation completes"
            }
        }


class WorkflowActionResponse(BaseModel):
    """Schema for workflow action response"""
    success: bool = Field(..., description="Whether action succeeded")
    workflow_id: UUID = Field(..., description="Workflow ID")
    action: str = Field(..., description="Action performed")
    new_status: str = Field(..., description="New workflow status")
    message: Optional[str] = Field(default=None, description="Response message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "workflow_id": "uuid-here",
                "action": "pause",
                "new_status": "paused",
                "message": "Workflow paused successfully"
            }
        }


class WorkflowStepUpdate(BaseModel):
    """Schema for updating a workflow step"""
    step_name: str = Field(..., description="Step name")
    status: str = Field(..., description="Step status (started, completed, failed)")
    output: Optional[Dict[str, Any]] = Field(default=None, description="Step output")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    duration_ms: Optional[float] = Field(default=None, description="Step duration")

    class Config:
        json_schema_extra = {
            "example": {
                "step_name": "extract_requirements",
                "status": "completed",
                "output": {"requirements_count": 15},
                "duration_ms": 2500.5
            }
        }
