"""Regulatory update model for tracking regulatory changes"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, Enum, Boolean
import enum
from app.db.postgres import Base


class RegulatorySource(str, enum.Enum):
    """Regulatory source enumeration"""
    FCA = "fca"
    PRA = "pra"
    BOE = "boe"
    EBA = "eba"
    OTHER = "other"


class RegulatoryUpdate(Base):
    """Regulatory update model for tracking regulatory changes and documents"""

    __tablename__ = "regulatory_updates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    source = Column(Enum(RegulatorySource), nullable=False, index=True)
    reference_number = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    published_date = Column(DateTime, nullable=False, index=True)
    effective_date = Column(DateTime, index=True)
    url = Column(Text)
    file_path = Column(String(500))
    is_processed = Column(Boolean, default=False, nullable=False, index=True)
    impact_level = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RegulatoryUpdate(id={self.id}, reference='{self.reference_number}', source='{self.source}')>"
