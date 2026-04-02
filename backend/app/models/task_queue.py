"""Task queue model for managing background agent tasks in PostgreSQL"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Integer, Text, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.postgres import Base


class TaskStatus(str, enum.Enum):
    """Task status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRY = "retry"


class TaskPriority(int, enum.Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


class TaskQueue(Base):
    """Task queue model for managing asynchronous agent tasks"""

    __tablename__ = "task_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    task_id = Column(String(255), unique=True, nullable=False, index=True)

    # Task identification
    agent_type = Column(String(100), nullable=False, index=True)
    task_type = Column(String(100), nullable=False, index=True)
    task_name = Column(String(255))

    # Status and priority
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)
    priority = Column(Integer, default=TaskPriority.MEDIUM.value, nullable=False, index=True)

    # Task data
    input_data = Column(JSON, nullable=False)
    result_data = Column(JSON)
    metadata = Column(JSON, default={})

    # Error handling
    error_message = Column(Text)
    error_traceback = Column(Text)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)

    # Progress tracking
    progress_percentage = Column(Integer, default=0)
    progress_message = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    started_at = Column(DateTime, index=True)
    completed_at = Column(DateTime, index=True)
    scheduled_for = Column(DateTime, index=True)  # For delayed tasks

    # User tracking
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    def __repr__(self):
        return f"<TaskQueue(id={self.id}, task_id='{self.task_id}', status='{self.status}', priority={self.priority})>"

    def to_dict(self):
        """Convert task to dictionary"""
        return {
            "id": str(self.id),
            "task_id": self.task_id,
            "agent_type": self.agent_type,
            "task_type": self.task_type,
            "task_name": self.task_name,
            "status": self.status.value if self.status else None,
            "priority": self.priority,
            "progress_percentage": self.progress_percentage,
            "progress_message": self.progress_message,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_by": str(self.created_by) if self.created_by else None,
        }
