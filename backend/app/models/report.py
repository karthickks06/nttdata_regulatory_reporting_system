"""Report model for storing generated regulatory reports"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, Enum, Boolean
import enum
from app.db.postgres import Base


class ReportStatus(str, enum.Enum):
    """Report status enumeration"""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SUBMITTED = "submitted"
    REJECTED = "rejected"


class ReportType(str, enum.Enum):
    """Report type enumeration"""
    COMPLIANCE = "compliance"
    VALIDATION = "validation"
    SUBMISSION = "submission"
    AUDIT = "audit"


class Report(Base):
    """Report model for storing generated regulatory reports and submissions"""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_name = Column(String(255), nullable=False)
    report_type = Column(Enum(ReportType), nullable=False, index=True)
    status = Column(Enum(ReportStatus), default=ReportStatus.DRAFT, nullable=False, index=True)
    description = Column(Text)
    file_path = Column(String(500))
    reporting_period_start = Column(DateTime)
    reporting_period_end = Column(DateTime)
    submission_deadline = Column(DateTime, index=True)
    submitted_at = Column(DateTime)
    approved_by = Column(Integer)
    approved_at = Column(DateTime)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Report(id={self.id}, name='{self.report_name}', type='{self.report_type}', status='{self.status}')>"
