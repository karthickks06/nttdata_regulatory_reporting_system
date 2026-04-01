"""Task queue model for managing background agent tasks in PostgreSQL"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, Enum
import enum
from app.db.postgres import Base


class TaskStatus(str, enum.Enum):
    """Task status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskQueue(Base):
    """Task queue model for managing asynchronous agent tasks"""

    __tablename__ = "task_queue"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(255), unique=True, nullable=False, index=True)
    agent_type = Column(String(100), nullable=False, index=True)
    task_type = Column(String(100), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)
    priority = Column(Integer, default=5, nullable=False)
    input_data = Column(Text, nullable=False)
    result_data = Column(Text)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_by = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<TaskQueue(id={self.id}, task_id='{self.task_id}', status='{self.status}')>"
