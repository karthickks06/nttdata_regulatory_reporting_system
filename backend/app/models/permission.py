"""Permission model for RBAC"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.postgres import Base
from app.models.role import role_permissions


class Permission(Base):
    """Permission model for fine-grained access control"""

    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    resource = Column(String(100), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)
    description = Column(Text)

    # Permission attributes
    is_system = Column(Boolean, default=False, nullable=False)  # System permissions cannot be deleted

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}', resource='{self.resource}', action='{self.action}')>"

    def to_dict(self):
        """Convert permission to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "resource": self.resource,
            "action": self.action,
            "description": self.description,
            "is_system": self.is_system,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
