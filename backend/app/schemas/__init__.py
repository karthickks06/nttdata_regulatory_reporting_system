"""Pydantic schemas for request/response validation"""

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.auth import Token, LoginRequest, TokenRefresh
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.schemas.regulatory_update import (
    RegulatoryUpdateCreate,
    RegulatoryUpdateUpdate,
    RegulatoryUpdateResponse
)
from app.schemas.requirement import (
    RequirementCreate,
    RequirementUpdate,
    RequirementResponse
)
from app.schemas.data_mapping import (
    DataMappingCreate,
    DataMappingUpdate,
    DataMappingResponse
)
from app.schemas.code import (
    GeneratedCodeCreate,
    GeneratedCodeUpdate,
    GeneratedCodeResponse,
    TestCaseCreate,
    TestCaseResponse
)
from app.schemas.report import (
    ReportCreate,
    ReportUpdate,
    ReportResponse
)
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse
)
from app.schemas.agent import (
    AgentTaskRequest,
    AgentTaskResponse,
    AgentStatus,
    AgentExecutionHistory,
    SubAgentRequest,
    SubAgentResponse,
    WorkflowExecutionRequest,
    WorkflowExecutionResponse,
    AgentMetrics
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Auth schemas
    "Token",
    "TokenRefresh",
    "LoginRequest",
    # Role schemas
    "RoleCreate",
    "RoleUpdate",
    "RoleResponse",
    # Permission schemas
    "PermissionCreate",
    "PermissionUpdate",
    "PermissionResponse",
    # Regulatory Update schemas
    "RegulatoryUpdateCreate",
    "RegulatoryUpdateUpdate",
    "RegulatoryUpdateResponse",
    # Requirement schemas
    "RequirementCreate",
    "RequirementUpdate",
    "RequirementResponse",
    # Data Mapping schemas
    "DataMappingCreate",
    "DataMappingUpdate",
    "DataMappingResponse",
    # Code schemas
    "GeneratedCodeCreate",
    "GeneratedCodeUpdate",
    "GeneratedCodeResponse",
    "TestCaseCreate",
    "TestCaseResponse",
    # Report schemas
    "ReportCreate",
    "ReportUpdate",
    "ReportResponse",
    # Workflow schemas
    "WorkflowCreate",
    "WorkflowUpdate",
    "WorkflowResponse",
    # Agent schemas
    "AgentTaskRequest",
    "AgentTaskResponse",
    "AgentStatus",
    "AgentExecutionHistory",
    "SubAgentRequest",
    "SubAgentResponse",
    "WorkflowExecutionRequest",
    "WorkflowExecutionResponse",
    "AgentMetrics",
]
