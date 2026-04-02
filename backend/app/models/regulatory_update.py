"""Regulatory update model for tracking regulatory changes"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.postgres import Base


class RegulatorySource(str, enum.Enum):
    """Regulatory source enumeration"""
    FCA = "fca"
    PRA = "pra"
    BOE = "boe"
    EBA = "eba"
    ESMA = "esma"
    BCBS = "bcbs"
    OTHER = "other"


class ImpactLevel(str, enum.Enum):
    """Impact level enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class ProcessingStatus(str, enum.Enum):
    """Processing status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class RegulatoryUpdate(Base):
    """Regulatory update model for tracking regulatory changes and documents"""

    __tablename__ = "regulatory_updates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    title = Column(String(500), nullable=False)
    source = Column(SQLEnum(RegulatorySource), nullable=False, index=True)
    reference_number = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)

    # Dates
    published_date = Column(DateTime, nullable=False, index=True)
    effective_date = Column(DateTime, index=True)
    deadline_date = Column(DateTime, index=True)

    # Links and files
    url = Column(Text)
    file_path = Column(String(500))
    document_hash = Column(String(64))  # SHA-256 hash for duplicate detection

    # Processing status
    is_processed = Column(Boolean, default=False, nullable=False, index=True)
    processing_status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING, index=True)
    impact_level = Column(SQLEnum(ImpactLevel), default=ImpactLevel.MEDIUM, index=True)

    # Metadata
    tags = Column(JSON, default=[])
    categories = Column(JSON, default=[])
    affected_systems = Column(JSON, default=[])
    extracted_requirements_count = Column(String(50), default="0")

    # User tracking
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime)

    # Relationships
    requirements = relationship("Requirement", back_populates="regulatory_update", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RegulatoryUpdate(id={self.id}, reference='{self.reference_number}', source='{self.source}')>"

    def to_dict(self):
        """Convert regulatory update to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "source": self.source.value if self.source else None,
            "reference_number": self.reference_number,
            "description": self.description,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "deadline_date": self.deadline_date.isoformat() if self.deadline_date else None,
            "url": self.url,
            "is_processed": self.is_processed,
            "processing_status": self.processing_status.value if self.processing_status else None,
            "impact_level": self.impact_level.value if self.impact_level else None,
            "tags": self.tags,
            "categories": self.categories,
            "extracted_requirements_count": self.extracted_requirements_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
