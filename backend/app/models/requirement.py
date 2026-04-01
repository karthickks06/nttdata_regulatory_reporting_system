"""Requirement model for storing parsed regulatory requirements"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean
from app.db.postgres import Base


class Requirement(Base):
    """Requirement model for storing individual regulatory requirements"""

    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    regulatory_update_id = Column(Integer, ForeignKey("regulatory_updates.id", ondelete="CASCADE"), nullable=False, index=True)
    requirement_text = Column(Text, nullable=False)
    section = Column(String(100))
    category = Column(String(100), index=True)
    priority = Column(String(50))
    is_mandatory = Column(Boolean, default=True, nullable=False)
    deadline = Column(DateTime)
    status = Column(String(50), default="pending", nullable=False, index=True)
    implementation_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Requirement(id={self.id}, category='{self.category}', status='{self.status}')>"
