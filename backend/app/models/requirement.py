"""Requirement model for storing parsed regulatory requirements"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.postgres import Base


class RequirementStatus(str, enum.Enum):
    """Requirement status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    MAPPED = "mapped"
    IMPLEMENTED = "implemented"
    VALIDATED = "validated"
    APPROVED = "approved"
    REJECTED = "rejected"


class RequirementPriority(str, enum.Enum):
    """Requirement priority enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RequirementCategory(str, enum.Enum):
    """Requirement category enumeration"""
    DATA_QUALITY = "data_quality"
    REPORTING = "reporting"
    VALIDATION = "validation"
    CALCULATION = "calculation"
    SUBMISSION = "submission"
    DOCUMENTATION = "documentation"
    OTHER = "other"


class Requirement(Base):
    """Requirement model for storing individual regulatory requirements"""

    __tablename__ = "requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    regulatory_update_id = Column(
        UUID(as_uuid=True),
        ForeignKey("regulatory_updates.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Requirement details
    requirement_id = Column(String(100), unique=True, index=True)  # External reference ID
    requirement_text = Column(Text, nullable=False)
    section = Column(String(100), index=True)
    sub_section = Column(String(100))
    category = Column(SQLEnum(RequirementCategory), default=RequirementCategory.OTHER, index=True)

    # Priority and status
    priority = Column(SQLEnum(RequirementPriority), default=RequirementPriority.MEDIUM, index=True)
    is_mandatory = Column(Boolean, default=True, nullable=False, index=True)
    status = Column(SQLEnum(RequirementStatus), default=RequirementStatus.PENDING, nullable=False, index=True)

    # Implementation details
    deadline = Column(DateTime, index=True)
    implementation_notes = Column(Text)
    technical_approach = Column(Text)
    affected_systems = Column(JSON, default=[])
    dependencies = Column(JSON, default=[])

    # Gap analysis
    has_gap = Column(Boolean, default=False, index=True)
    gap_description = Column(Text)
    gap_severity = Column(String(50))

    # User tracking
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)

    # Relationships
    regulatory_update = relationship("RegulatoryUpdate", back_populates="requirements")
    data_mappings = relationship("DataMapping", back_populates="requirement", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Requirement(id={self.id}, category='{self.category}', status='{self.status}')>"

    def to_dict(self):
        """Convert requirement to dictionary"""
        return {
            "id": str(self.id),
            "regulatory_update_id": str(self.regulatory_update_id),
            "requirement_id": self.requirement_id,
            "requirement_text": self.requirement_text,
            "section": self.section,
            "sub_section": self.sub_section,
            "category": self.category.value if self.category else None,
            "priority": self.priority.value if self.priority else None,
            "is_mandatory": self.is_mandatory,
            "status": self.status.value if self.status else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "has_gap": self.has_gap,
            "gap_description": self.gap_description,
            "affected_systems": self.affected_systems,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
