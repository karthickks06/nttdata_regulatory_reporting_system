"""
Base database module - imports all models for SQLAlchemy metadata registration.

This module must import all SQLAlchemy models so they are registered with Base.metadata.
This allows Alembic migrations and create_all() to work correctly.
"""

from app.db.postgres import Base

# Import all models to register them with Base.metadata
# Authentication & Authorization (4 models)
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.session import Session

# System Infrastructure (3 models)
from app.models.cache import Cache
from app.models.rate_limit import RateLimit
from app.models.task_queue import TaskQueue

# Regulatory Compliance (3 models)
from app.models.regulatory_update import RegulatoryUpdate
from app.models.requirement import Requirement
from app.models.data_mapping import DataMapping

# Development & Testing (2 models)
from app.models.generated_code import GeneratedCode
from app.models.test_case import TestCase

# Reporting & Workflow (2 models)
from app.models.report import Report
from app.models.workflow import Workflow

# File Management & Audit (2 models)
from app.models.file_metadata import FileMetadata
from app.models.audit_log import AuditLog

# Total: 16 models

__all__ = [
    "Base",
    # Auth models
    "User",
    "Role",
    "Permission",
    "Session",
    # System models
    "Cache",
    "RateLimit",
    "TaskQueue",
    # Compliance models
    "RegulatoryUpdate",
    "Requirement",
    "DataMapping",
    # Dev models
    "GeneratedCode",
    "TestCase",
    # Reporting models
    "Report",
    "Workflow",
    # File & Audit models
    "FileMetadata",
    "AuditLog",
]
