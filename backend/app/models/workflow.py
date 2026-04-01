"""Workflow model for orchestrating multi-step processes"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, Enum, JSON
import enum
from app.db.postgres import Base


class WorkflowStatus(str, enum.Enum):
    """Workflow status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Workflow(Base):
    """Workflow model for orchestrating multi-step agent processes"""

    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    workflow_name = Column(String(255), nullable=False)
    workflow_type = Column(String(100), nullable=False, index=True)
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.PENDING, nullable=False, index=True)
    description = Column(Text)
    definition = Column(JSON)  # Workflow definition (steps, dependencies)
    state = Column(JSON)  # Current workflow state
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.workflow_name}', status='{self.status}')>"
