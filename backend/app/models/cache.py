"""Cache model for storing application cache in PostgreSQL (replaces Redis)"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.postgres import Base


class Cache(Base):
    """Cache model for storing key-value pairs with expiration"""

    __tablename__ = "cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    metadata = Column(JSON, default={})

    # Expiration
    expires_at = Column(DateTime, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Cache(id={self.id}, key='{self.key}')>"

    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        """Convert cache to dictionary"""
        return {
            "id": str(self.id),
            "key": self.key,
            "value": self.value,
            "metadata": self.metadata,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_expired": self.is_expired(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
