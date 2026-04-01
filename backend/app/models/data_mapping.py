"""Data mapping model for storing source-to-target data mappings"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean
from app.db.postgres import Base


class DataMapping(Base):
    """Data mapping model for storing data lineage and transformation rules"""

    __tablename__ = "data_mappings"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False, index=True)
    source_system = Column(String(200), nullable=False, index=True)
    source_table = Column(String(200), nullable=False)
    source_column = Column(String(200), nullable=False)
    target_field = Column(String(200), nullable=False, index=True)
    transformation_rule = Column(Text)
    validation_rule = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<DataMapping(id={self.id}, source='{self.source_system}.{self.source_table}.{self.source_column}', target='{self.target_field}')>"
