"""File metadata model for tracking uploaded and generated files"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, BigInteger, ForeignKey, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.postgres import Base


class FileType(str, enum.Enum):
    """File type enumeration"""
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    PDF = "pdf"
    IMAGE = "image"
    CODE = "code"
    REPORT = "report"
    ARCHIVE = "archive"
    OTHER = "other"


class StorageLocation(str, enum.Enum):
    """Storage location enumeration"""
    DOCUMENTS = "documents"
    REPORTS = "reports"
    UPLOADS = "uploads"
    TEMP = "temp"
    ARCHIVE = "archive"
    GENERATED = "generated"


class FileStatus(str, enum.Enum):
    """File status enumeration"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    PROCESSING = "processing"


class FileMetadata(Base):
    """File metadata model for tracking all files in the system"""

    __tablename__ = "file_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # File identification
    file_name = Column(String(255), nullable=False, index=True)
    original_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False, unique=True, index=True)
    file_extension = Column(String(50))

    # File type and classification
    file_type = Column(SQLEnum(FileType), nullable=False, index=True)
    mime_type = Column(String(100))
    content_type = Column(String(100))

    # File size and hash
    file_size = Column(BigInteger, nullable=False)  # In bytes
    file_hash = Column(String(64), index=True)  # SHA-256 hash for duplicate detection
    checksum = Column(String(32))  # MD5 checksum

    # Storage information
    storage_location = Column(SQLEnum(StorageLocation), nullable=False, index=True)
    storage_path = Column(String(500))  # Full storage path
    is_encrypted = Column(Boolean, default=False)
    encryption_key_id = Column(String(255))

    # File status
    status = Column(SQLEnum(FileStatus), default=FileStatus.ACTIVE, nullable=False, index=True)
    is_temporary = Column(Boolean, default=False)
    expires_at = Column(DateTime)  # For temporary files
    is_public = Column(Boolean, default=False)

    # Processing information
    is_processed = Column(Boolean, default=False, index=True)
    processing_status = Column(String(50))
    processing_error = Column(String(500))
    extracted_text = Column(String(500))  # For search

    # Relationships
    related_entity_type = Column(String(100))  # e.g., "regulatory_update", "report"
    related_entity_id = Column(UUID(as_uuid=True))

    # Version control
    version = Column(String(50), default="1.0")
    parent_file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id", ondelete="SET NULL"), nullable=True)

    # Metadata
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    custom_properties = Column(JSON, default={})

    # User tracking
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    accessed_at = Column(DateTime)  # Last access time
    deleted_at = Column(DateTime)

    def __repr__(self):
        return f"<FileMetadata(id={self.id}, name='{self.file_name}', path='{self.file_path}', status='{self.status}')>"

    def to_dict(self):
        """Convert file metadata to dictionary"""
        return {
            "id": str(self.id),
            "file_name": self.file_name,
            "original_name": self.original_name,
            "file_path": self.file_path,
            "file_extension": self.file_extension,
            "file_type": self.file_type.value if self.file_type else None,
            "mime_type": self.mime_type,
            "file_size": str(self.file_size),
            "file_hash": self.file_hash,
            "storage_location": self.storage_location.value if self.storage_location else None,
            "status": self.status.value if self.status else None,
            "is_processed": self.is_processed,
            "version": self.version,
            "uploaded_by": str(self.uploaded_by) if self.uploaded_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
