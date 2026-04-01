"""Generated code model for storing AI-generated SQL and Python code"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean, Enum
import enum
from app.db.postgres import Base


class CodeType(str, enum.Enum):
    """Code type enumeration"""
    SQL = "sql"
    PYTHON = "python"
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"


class GeneratedCode(Base):
    """Generated code model for storing AI-generated code artifacts"""

    __tablename__ = "generated_code"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False, index=True)
    code_type = Column(Enum(CodeType), nullable=False, index=True)
    code_content = Column(Text, nullable=False)
    description = Column(Text)
    file_path = Column(String(500))
    is_validated = Column(Boolean, default=False, nullable=False)
    is_deployed = Column(Boolean, default=False, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<GeneratedCode(id={self.id}, type='{self.code_type}', version={self.version})>"
