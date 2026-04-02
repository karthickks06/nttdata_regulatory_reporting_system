"""Session model for managing user sessions (replaces Redis)"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class Session(Base):
    """Session model for storing user session data in PostgreSQL"""

    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Token and device info
    token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    device_id = Column(String(255))
    device_name = Column(String(255))

    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_revoked = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    revoked_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(id={self.id}, session_id='{self.session_id}', user_id={self.user_id})>"

    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        """Convert session to dictionary"""
        return {
            "id": str(self.id),
            "session_id": self.session_id,
            "user_id": str(self.user_id),
            "ip_address": self.ip_address,
            "device_name": self.device_name,
            "is_active": self.is_active,
            "is_revoked": self.is_revoked,
            "is_expired": self.is_expired(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
        }
