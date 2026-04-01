"""Base database module - imports all models"""

from app.db.postgres import Base

# Import all models to register them with Base.metadata
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.session import Session
from app.models.cache import Cache
from app.models.rate_limit import RateLimit
from app.models.task_queue import TaskQueue
from app.models.regulatory_update import RegulatoryUpdate
from app.models.requirement import Requirement
from app.models.data_mapping import DataMapping
from app.models.generated_code import GeneratedCode
from app.models.test_case import TestCase
from app.models.report import Report
from app.models.workflow import Workflow
from app.models.file_metadata import FileMetadata
from app.models.audit_log import AuditLog

__all__ = ["Base"]
