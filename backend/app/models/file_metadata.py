"""File metadata model for tracking uploaded and generated files"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from app.db.postgres import Base


class FileMetadata(Base):
    """File metadata model for tracking all files in the system"""

    __tablename__ = "file_metadata"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False, unique=True, index=True)
    file_type = Column(String(100), nullable=False, index=True)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100))
    storage_location = Column(String(100), nullable=False)  # e.g., "documents", "reports", "temp"
    uploaded_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<FileMetadata(id={self.id}, name='{self.file_name}', path='{self.file_path}')>"
