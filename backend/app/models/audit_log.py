"""Audit log model for tracking all system actions"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.postgres import Base


class AuditAction(str, enum.Enum):
    """Audit action types"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    APPROVE = "approve"
    REJECT = "reject"
    EXECUTE = "execute"
    GENERATE = "generate"
    VALIDATE = "validate"
    EXPORT = "export"


class AuditStatus(str, enum.Enum):
    """Audit status types"""
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
    ERROR = "error"


class AuditLog(Base):
    """Audit log model for tracking all user actions and system events"""

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Action details
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    status = Column(SQLEnum(AuditStatus), nullable=False, default=AuditStatus.SUCCESS, index=True)

    # Description and context
    description = Column(Text)
    details = Column(JSON, default={})

    # Request information
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_method = Column(String(10))
    request_path = Column(String(500))
    request_data = Column(JSON)

    # Response information
    response_status = Column(String(50))
    response_data = Column(JSON)
    error_message = Column(Text)

    # Timing
    execution_time_ms = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', resource='{self.resource_type}', status='{self.status}')>"

    def to_dict(self):
        """Convert audit log to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "action": self.action.value if self.action else None,
            "resource_type": self.resource_type,
            "resource_id": str(self.resource_id) if self.resource_id else None,
            "status": self.status.value if self.status else None,
            "description": self.description,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "request_method": self.request_method,
            "request_path": self.request_path,
            "execution_time_ms": self.execution_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
