"""Data mapping model for storing source-to-target data mappings"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class DataMapping(Base):
    """Data mapping model for storing data lineage and transformation rules"""

    __tablename__ = "data_mappings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    requirement_id = Column(
        UUID(as_uuid=True),
        ForeignKey("requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Source information
    source_system = Column(String(200), nullable=False, index=True)
    source_schema = Column(String(200))
    source_table = Column(String(200), nullable=False, index=True)
    source_column = Column(String(200), nullable=False, index=True)
    source_data_type = Column(String(100))

    # Target information
    target_system = Column(String(200))
    target_schema = Column(String(200))
    target_table = Column(String(200))
    target_field = Column(String(200), nullable=False, index=True)
    target_data_type = Column(String(100))

    # Transformation and validation
    transformation_rule = Column(Text)
    transformation_logic = Column(JSON)  # Structured transformation steps
    validation_rule = Column(Text)
    validation_logic = Column(JSON)  # Structured validation rules

    # Business logic
    business_rule_description = Column(Text)
    calculation_formula = Column(Text)
    data_quality_rules = Column(JSON, default=[])

    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_validated = Column(Boolean, default=False, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)

    # Metadata
    confidence_score = Column(String(50))  # For AI-generated mappings
    mapping_notes = Column(Text)
    tags = Column(JSON, default=[])

    # User tracking
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime)

    # Relationships
    requirement = relationship("Requirement", back_populates="data_mappings")

    def __repr__(self):
        return f"<DataMapping(id={self.id}, source='{self.source_system}.{self.source_table}.{self.source_column}', target='{self.target_field}')>"

    def to_dict(self):
        """Convert data mapping to dictionary"""
        return {
            "id": str(self.id),
            "requirement_id": str(self.requirement_id),
            "source_system": self.source_system,
            "source_table": self.source_table,
            "source_column": self.source_column,
            "source_data_type": self.source_data_type,
            "target_field": self.target_field,
            "target_data_type": self.target_data_type,
            "transformation_rule": self.transformation_rule,
            "validation_rule": self.validation_rule,
            "is_active": self.is_active,
            "is_validated": self.is_validated,
            "is_approved": self.is_approved,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
