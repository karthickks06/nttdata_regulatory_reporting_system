"""Test case model for storing test scenarios and results"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.postgres import Base


class TestStatus(str, enum.Enum):
    """Test status enumeration"""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestType(str, enum.Enum):
    """Test type enumeration"""
    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    REGRESSION = "regression"


class TestCase(Base):
    """Test case model for storing test scenarios and execution results"""

    __tablename__ = "test_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    generated_code_id = Column(
        UUID(as_uuid=True),
        ForeignKey("generated_code.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Test identification
    test_name = Column(String(255), nullable=False, index=True)
    test_description = Column(Text)
    test_type = Column(SQLEnum(TestType), default=TestType.UNIT, index=True)

    # Test data
    test_input = Column(JSON)  # Structured test input data
    expected_output = Column(JSON)  # Structured expected output
    actual_output = Column(JSON)  # Structured actual output
    test_data_setup = Column(Text)  # SQL or code to set up test data
    test_data_teardown = Column(Text)  # SQL or code to clean up test data

    # Test execution
    status = Column(SQLEnum(TestStatus), default=TestStatus.PENDING, nullable=False, index=True)
    error_message = Column(Text)
    error_traceback = Column(Text)
    execution_time_ms = Column(String(50))
    assertions = Column(JSON, default=[])  # List of assertions and their results

    # Test configuration
    timeout_seconds = Column(String(50), default="30")
    retry_count = Column(String(50), default="0")
    is_automated = Column(String(50), default="true")

    # Coverage and metrics
    coverage_percentage = Column(String(50))
    complexity_covered = Column(JSON, default=[])

    # User tracking
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    executed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    executed_at = Column(DateTime, index=True)

    # Relationships
    generated_code = relationship("GeneratedCode", back_populates="test_cases")

    def __repr__(self):
        return f"<TestCase(id={self.id}, name='{self.test_name}', status='{self.status}')>"

    def to_dict(self):
        """Convert test case to dictionary"""
        return {
            "id": str(self.id),
            "generated_code_id": str(self.generated_code_id),
            "test_name": self.test_name,
            "test_description": self.test_description,
            "test_type": self.test_type.value if self.test_type else None,
            "status": self.status.value if self.status else None,
            "error_message": self.error_message,
            "execution_time_ms": self.execution_time_ms,
            "coverage_percentage": self.coverage_percentage,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
