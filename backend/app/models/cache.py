"""Cache model for storing application cache in PostgreSQL (replaces Redis)"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text
from app.db.postgres import Base


class Cache(Base):
    """Cache model for storing key-value pairs with expiration"""

    __tablename__ = "cache"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Cache(id={self.id}, key='{self.key}')>"
