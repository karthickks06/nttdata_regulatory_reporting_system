"""Rate limit model for API rate limiting in PostgreSQL (replaces Redis)"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from app.db.postgres import Base


class RateLimit(Base):
    """Rate limit model for tracking API request counts"""

    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(255), nullable=False, index=True)  # IP address or user ID
    endpoint = Column(String(255), nullable=False, index=True)
    request_count = Column(Integer, default=1, nullable=False)
    window_start = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)

    def __repr__(self):
        return f"<RateLimit(id={self.id}, identifier='{self.identifier}', endpoint='{self.endpoint}', count={self.request_count})>"
