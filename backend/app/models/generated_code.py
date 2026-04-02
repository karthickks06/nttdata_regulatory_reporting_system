"""Generated code model for storing AI-generated SQL and Python code"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Enum as SQLEnum, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.postgres import Base


class CodeType(str, enum.Enum):
    """Code type enumeration"""
    SQL = "sql"
    PYTHON = "python"
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"
    STORED_PROCEDURE = "stored_procedure"
    VIEW = "view"
    TRIGGER = "trigger"


class CodeStatus(str, enum.Enum):
    """Code status enumeration"""
    DRAFT = "draft"
    VALIDATED = "validated"
    APPROVED = "approved"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"


class GeneratedCode(Base):
    """Generated code model for storing AI-generated code artifacts"""

    __tablename__ = "generated_code"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    requirement_id = Column(
        UUID(as_uuid=True),
        ForeignKey("requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Code details
    code_type = Column(SQLEnum(CodeType), nullable=False, index=True)
    language = Column(String(50))  # python, sql, etc.
    code_content = Column(Text, nullable=False)
    description = Column(Text)
    title = Column(String(500))

    # File information
    file_path = Column(String(500))
    file_name = Column(String(255))

    # Status and validation
    status = Column(SQLEnum(CodeStatus), default=CodeStatus.DRAFT, nullable=False, index=True)
    is_validated = Column(Boolean, default=False, nullable=False, index=True)
    is_deployed = Column(Boolean, default=False, nullable=False, index=True)
    validation_errors = Column(JSON, default=[])
    validation_warnings = Column(JSON, default=[])

    # Versioning
    version = Column(Integer, default=1, nullable=False, index=True)
    parent_version_id = Column(UUID(as_uuid=True), ForeignKey("generated_code.id", ondelete="SET NULL"), nullable=True)

    # Performance and complexity
    complexity_score = Column(String(50))
    estimated_execution_time = Column(String(50))
    dependencies = Column(JSON, default=[])

    # Metadata
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    generation_prompt = Column(Text)  # The prompt used to generate the code

    # User tracking
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    validated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deployed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    validated_at = Column(DateTime)
    deployed_at = Column(DateTime)

    # Relationships
    test_cases = relationship("TestCase", back_populates="generated_code", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<GeneratedCode(id={self.id}, type='{self.code_type}', version={self.version}, status='{self.status}')>"

    def to_dict(self):
        """Convert generated code to dictionary"""
        return {
            "id": str(self.id),
            "requirement_id": str(self.requirement_id),
            "code_type": self.code_type.value if self.code_type else None,
            "language": self.language,
            "title": self.title,
            "description": self.description,
            "status": self.status.value if self.status else None,
            "is_validated": self.is_validated,
            "is_deployed": self.is_deployed,
            "version": self.version,
            "validation_errors": self.validation_errors,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
