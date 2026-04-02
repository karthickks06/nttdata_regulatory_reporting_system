"""Workflow model for orchestrating multi-step processes"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Integer, Text, Enum as SQLEnum, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.postgres import Base


class WorkflowStatus(str, enum.Enum):
    """Workflow status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class WorkflowType(str, enum.Enum):
    """Workflow type enumeration"""
    REGULATORY_PROCESSING = "regulatory_processing"
    CODE_GENERATION = "code_generation"
    REPORT_GENERATION = "report_generation"
    VALIDATION = "validation"
    APPROVAL = "approval"
    CUSTOM = "custom"


class WorkflowPriority(int, enum.Enum):
    """Workflow priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class Workflow(Base):
    """Workflow model for orchestrating multi-step agent processes"""

    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    workflow_name = Column(String(255), nullable=False, index=True)
    workflow_type = Column(SQLEnum(WorkflowType), nullable=False, index=True)
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.PENDING, nullable=False, index=True)
    priority = Column(Integer, default=WorkflowPriority.MEDIUM.value, index=True)
    description = Column(Text)

    # Workflow definition and state
    definition = Column(JSON)  # Workflow definition (steps, dependencies, conditions)
    state = Column(JSON, default={})  # Current workflow state
    context = Column(JSON, default={})  # Shared context across steps
    variables = Column(JSON, default={})  # Workflow variables

    # Input/output data
    input_data = Column(JSON)
    output_data = Column(JSON)
    intermediate_results = Column(JSON, default={})

    # Error handling
    error_message = Column(Text)
    error_traceback = Column(Text)
    error_step = Column(String(100))
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    # Progress tracking
    current_step = Column(String(50), default="0")
    current_step_name = Column(String(255))
    total_steps = Column(String(50), default="0")
    progress_percentage = Column(Integer, default=0)
    step_history = Column(JSON, default=[])  # History of completed steps

    # Timing
    estimated_duration_seconds = Column(String(50))
    actual_duration_seconds = Column(String(50))
    timeout_seconds = Column(String(50))

    # Approval workflow
    requires_approval = Column(String(50), default="false")
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime)
    approval_notes = Column(Text)

    # Timestamps
    started_at = Column(DateTime, index=True)
    completed_at = Column(DateTime, index=True)
    paused_at = Column(DateTime)
    cancelled_at = Column(DateTime)

    # User tracking
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Metadata
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})

    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.workflow_name}', type='{self.workflow_type}', status='{self.status}')>"

    def to_dict(self):
        """Convert workflow to dictionary"""
        return {
            "id": str(self.id),
            "workflow_name": self.workflow_name,
            "workflow_type": self.workflow_type.value if self.workflow_type else None,
            "status": self.status.value if self.status else None,
            "priority": self.priority,
            "description": self.description,
            "current_step": self.current_step,
            "current_step_name": self.current_step_name,
            "total_steps": self.total_steps,
            "progress_percentage": self.progress_percentage,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
