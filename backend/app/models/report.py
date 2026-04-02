"""Report model for storing generated regulatory reports"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.postgres import Base


class ReportStatus(str, enum.Enum):
    """Report status enumeration"""
    DRAFT = "draft"
    GENERATING = "generating"
    VALIDATING = "validating"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SUBMITTED = "submitted"
    REJECTED = "rejected"
    FAILED = "failed"


class ReportType(str, enum.Enum):
    """Report type enumeration"""
    COMPLIANCE = "compliance"
    VALIDATION = "validation"
    SUBMISSION = "submission"
    AUDIT = "audit"
    GAP_ANALYSIS = "gap_analysis"
    IMPACT_ASSESSMENT = "impact_assessment"


class ReportFormat(str, enum.Enum):
    """Report format enumeration"""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    XML = "xml"


class Report(Base):
    """Report model for storing generated regulatory reports and submissions"""

    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    report_name = Column(String(255), nullable=False, index=True)
    report_type = Column(SQLEnum(ReportType), nullable=False, index=True)
    report_format = Column(SQLEnum(ReportFormat), default=ReportFormat.PDF)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.DRAFT, nullable=False, index=True)
    description = Column(Text)

    # File information
    file_path = Column(String(500))
    file_name = Column(String(255))
    file_size = Column(String(50))  # In bytes
    file_hash = Column(String(64))  # SHA-256 hash

    # Reporting period
    reporting_period_start = Column(DateTime, index=True)
    reporting_period_end = Column(DateTime, index=True)
    submission_deadline = Column(DateTime, index=True)
    reminder_sent = Column(String(50), default="false")

    # Report data
    report_data = Column(JSON)  # Structured report data
    validation_results = Column(JSON, default=[])
    anomalies_detected = Column(JSON, default=[])
    quality_score = Column(String(50))

    # Submission tracking
    submission_reference = Column(String(255))
    submission_confirmation = Column(String(255))
    submitted_at = Column(DateTime, index=True)
    submission_response = Column(JSON)

    # Approval workflow
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime)
    rejection_reason = Column(Text)
    approval_notes = Column(Text)

    # User tracking
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    generated_at = Column(DateTime)
    validated_at = Column(DateTime)

    # Metadata
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    version = Column(String(50), default="1.0")

    def __repr__(self):
        return f"<Report(id={self.id}, name='{self.report_name}', type='{self.report_type}', status='{self.status}')>"

    def to_dict(self):
        """Convert report to dictionary"""
        return {
            "id": str(self.id),
            "report_name": self.report_name,
            "report_type": self.report_type.value if self.report_type else None,
            "report_format": self.report_format.value if self.report_format else None,
            "status": self.status.value if self.status else None,
            "description": self.description,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "reporting_period_start": self.reporting_period_start.isoformat() if self.reporting_period_start else None,
            "reporting_period_end": self.reporting_period_end.isoformat() if self.reporting_period_end else None,
            "submission_deadline": self.submission_deadline.isoformat() if self.submission_deadline else None,
            "quality_score": self.quality_score,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
