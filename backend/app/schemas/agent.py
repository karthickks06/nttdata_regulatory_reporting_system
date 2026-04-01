"""Agent execution schemas"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


class AgentTaskRequest(BaseModel):
    """Schema for agent task request"""
    agent_name: str
    task_type: str
    input_data: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None


class AgentTaskResponse(BaseModel):
    """Schema for agent task response"""
    success: bool
    agent_name: str
    task_type: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    executed_at: datetime


class AgentStatus(BaseModel):
    """Schema for agent status"""
    agent_name: str
    level: int
    status: str
    is_active: bool
    tasks_executed: int
    last_execution: Optional[datetime]


class AgentExecutionHistory(BaseModel):
    """Schema for agent execution history"""
    agent_name: str
    action: str
    timestamp: datetime
    status: str
    details: Optional[Dict[str, Any]] = None


class SubAgentRequest(BaseModel):
    """Schema for sub-agent request"""
    sub_agent_type: str  # document_parser, sql_generator, etc.
    operation: str
    parameters: Dict[str, Any]


class SubAgentResponse(BaseModel):
    """Schema for sub-agent response"""
    success: bool
    sub_agent_type: str
    operation: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
