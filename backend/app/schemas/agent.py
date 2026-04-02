"""Agent execution schemas"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class AgentTaskRequest(BaseModel):
    """Schema for agent task request"""
    agent_name: str = Field(..., description="Name of the agent to execute")
    task_type: str = Field(..., description="Type of task to perform")
    input_data: Dict[str, Any] = Field(..., description="Input data for the task")
    priority: Optional[int] = Field(default=3, ge=1, le=5, description="Task priority (1=highest, 5=lowest)")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Additional options")
    timeout_seconds: Optional[int] = Field(default=300, description="Task timeout in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "compliance_agent",
                "task_type": "process_regulatory_update",
                "input_data": {"update_id": "uuid-here"},
                "priority": 2,
                "options": {"auto_approve": False}
            }
        }


class AgentTaskResponse(BaseModel):
    """Schema for agent task response"""
    success: bool = Field(..., description="Whether the task succeeded")
    task_id: str = Field(..., description="Unique task identifier")
    agent_name: str = Field(..., description="Name of the agent that executed")
    task_type: str = Field(..., description="Type of task performed")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Task result data")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    error_traceback: Optional[str] = Field(default=None, description="Error traceback if failed")
    execution_time_ms: Optional[float] = Field(default=None, description="Execution time in milliseconds")
    executed_at: datetime = Field(..., description="Task execution timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "task_id": "task-uuid",
                "agent_name": "compliance_agent",
                "task_type": "process_regulatory_update",
                "result": {"requirements_extracted": 15},
                "error": None,
                "execution_time_ms": 1250.5,
                "executed_at": "2026-04-02T10:30:00Z"
            }
        }


class AgentStatus(BaseModel):
    """Schema for agent status"""
    agent_name: str = Field(..., description="Agent name")
    agent_type: str = Field(..., description="Agent type/class")
    level: int = Field(..., description="Agent hierarchy level (0=master, 1=supervisor, 2=worker)")
    status: str = Field(..., description="Current status (active, idle, busy, error)")
    is_active: bool = Field(..., description="Whether agent is active")
    is_available: bool = Field(..., description="Whether agent is available for tasks")
    tasks_queued: int = Field(default=0, description="Number of queued tasks")
    tasks_running: int = Field(default=0, description="Number of running tasks")
    tasks_completed: int = Field(default=0, description="Number of completed tasks")
    tasks_failed: int = Field(default=0, description="Number of failed tasks")
    last_execution: Optional[datetime] = Field(default=None, description="Last execution timestamp")
    average_execution_time_ms: Optional[float] = Field(default=None, description="Average execution time")
    success_rate: Optional[float] = Field(default=None, description="Success rate percentage")

    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "compliance_agent",
                "agent_type": "ComplianceAgent",
                "level": 0,
                "status": "active",
                "is_active": True,
                "is_available": True,
                "tasks_queued": 2,
                "tasks_running": 1,
                "tasks_completed": 150,
                "tasks_failed": 3,
                "success_rate": 98.0
            }
        }


class AgentExecutionHistory(BaseModel):
    """Schema for agent execution history"""
    id: UUID = Field(..., description="Execution history ID")
    agent_name: str = Field(..., description="Agent name")
    action: str = Field(..., description="Action performed")
    timestamp: datetime = Field(..., description="Execution timestamp")
    status: str = Field(..., description="Execution status (success, failure, pending)")
    duration_ms: Optional[float] = Field(default=None, description="Execution duration in milliseconds")
    input_summary: Optional[str] = Field(default=None, description="Summary of input data")
    output_summary: Optional[str] = Field(default=None, description="Summary of output data")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional execution details")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "agent_name": "ba_supervisor",
                "action": "review_requirements",
                "timestamp": "2026-04-02T10:30:00Z",
                "status": "success",
                "duration_ms": 2500.0,
                "input_summary": "Reviewed 15 requirements",
                "output_summary": "Approved 14, rejected 1"
            }
        }


class SubAgentRequest(BaseModel):
    """Schema for sub-agent request"""
    sub_agent_type: str = Field(..., description="Sub-agent type (document_parser, sql_generator, etc.)")
    operation: str = Field(..., description="Operation to perform")
    parameters: Dict[str, Any] = Field(..., description="Operation parameters")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

    class Config:
        json_schema_extra = {
            "example": {
                "sub_agent_type": "document_parser",
                "operation": "parse_pdf",
                "parameters": {"file_path": "/path/to/doc.pdf"},
                "context": {"language": "en"}
            }
        }


class SubAgentResponse(BaseModel):
    """Schema for sub-agent response"""
    success: bool = Field(..., description="Whether operation succeeded")
    sub_agent_type: str = Field(..., description="Sub-agent type that executed")
    operation: str = Field(..., description="Operation performed")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Operation result")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    warnings: Optional[List[str]] = Field(default=None, description="Warning messages")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "sub_agent_type": "document_parser",
                "operation": "parse_pdf",
                "result": {"pages": 25, "text_length": 15000},
                "error": None,
                "warnings": ["Page 5 had low OCR confidence"]
            }
        }


class WorkflowExecutionRequest(BaseModel):
    """Schema for workflow execution request"""
    workflow_type: str = Field(..., description="Type of workflow to execute")
    input_data: Dict[str, Any] = Field(..., description="Workflow input data")
    priority: Optional[int] = Field(default=3, description="Workflow priority")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Workflow options")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_type": "regulatory_processing",
                "input_data": {"update_id": "uuid-here"},
                "priority": 2,
                "options": {"auto_deploy": False}
            }
        }


class WorkflowExecutionResponse(BaseModel):
    """Schema for workflow execution response"""
    workflow_id: UUID = Field(..., description="Workflow execution ID")
    workflow_type: str = Field(..., description="Workflow type")
    status: str = Field(..., description="Current workflow status")
    current_step: str = Field(..., description="Current workflow step")
    progress_percentage: int = Field(..., description="Progress percentage (0-100)")
    started_at: datetime = Field(..., description="Workflow start time")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion time")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "uuid-here",
                "workflow_type": "regulatory_processing",
                "status": "running",
                "current_step": "requirement_extraction",
                "progress_percentage": 35,
                "started_at": "2026-04-02T10:30:00Z"
            }
        }


class AgentMetrics(BaseModel):
    """Schema for agent performance metrics"""
    agent_name: str = Field(..., description="Agent name")
    total_tasks: int = Field(..., description="Total tasks executed")
    successful_tasks: int = Field(..., description="Successfully completed tasks")
    failed_tasks: int = Field(..., description="Failed tasks")
    average_duration_ms: float = Field(..., description="Average task duration in milliseconds")
    min_duration_ms: float = Field(..., description="Minimum task duration")
    max_duration_ms: float = Field(..., description="Maximum task duration")
    success_rate: float = Field(..., description="Success rate percentage")
    tasks_last_24h: int = Field(..., description="Tasks in last 24 hours")
    tasks_last_7d: int = Field(..., description="Tasks in last 7 days")

    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "compliance_agent",
                "total_tasks": 1500,
                "successful_tasks": 1475,
                "failed_tasks": 25,
                "average_duration_ms": 2350.5,
                "min_duration_ms": 150.2,
                "max_duration_ms": 15000.0,
                "success_rate": 98.33,
                "tasks_last_24h": 45,
                "tasks_last_7d": 320
            }
        }
