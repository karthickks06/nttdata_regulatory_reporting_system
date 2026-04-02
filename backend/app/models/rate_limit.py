"""Rate limit model for API rate limiting in PostgreSQL (replaces Redis)"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.postgres import Base


class RateLimit(Base):
    """Rate limit model for tracking API request counts"""

    __tablename__ = "rate_limits"
    __table_args__ = (
        UniqueConstraint('identifier', 'endpoint', 'window_start', name='uq_rate_limit'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    identifier = Column(String(255), nullable=False, index=True)  # IP address or user ID
    endpoint = Column(String(255), nullable=False, index=True)
    request_count = Column(Integer, default=1, nullable=False)
    limit_per_window = Column(Integer, nullable=False)  # Max requests allowed
    window_size_seconds = Column(Integer, nullable=False)  # Window size in seconds

    # Timestamps
    window_start = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RateLimit(id={self.id}, identifier='{self.identifier}', endpoint='{self.endpoint}', count={self.request_count}/{self.limit_per_window})>"

    def is_expired(self) -> bool:
        """Check if rate limit window is expired"""
        return datetime.utcnow() > self.expires_at

    def is_exceeded(self) -> bool:
        """Check if rate limit is exceeded"""
        return self.request_count >= self.limit_per_window

    def to_dict(self):
        """Convert rate limit to dictionary"""
        return {
            "id": str(self.id),
            "identifier": self.identifier,
            "endpoint": self.endpoint,
            "request_count": self.request_count,
            "limit_per_window": self.limit_per_window,
            "window_size_seconds": self.window_size_seconds,
            "is_exceeded": self.is_exceeded(),
            "is_expired": self.is_expired(),
            "window_start": self.window_start.isoformat() if self.window_start else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
