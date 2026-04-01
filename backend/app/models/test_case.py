"""Test case model for storing test scenarios and results"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean, Enum
import enum
from app.db.postgres import Base


class TestStatus(str, enum.Enum):
    """Test status enumeration"""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TestCase(Base):
    """Test case model for storing test scenarios and execution results"""

    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    generated_code_id = Column(Integer, ForeignKey("generated_code.id", ondelete="CASCADE"), nullable=False, index=True)
    test_name = Column(String(255), nullable=False)
    test_description = Column(Text)
    test_input = Column(Text)
    expected_output = Column(Text)
    actual_output = Column(Text)
    status = Column(Enum(TestStatus), default=TestStatus.PENDING, nullable=False, index=True)
    error_message = Column(Text)
    execution_time_ms = Column(Integer)
    executed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<TestCase(id={self.id}, name='{self.test_name}', status='{self.status}')>"
