"""
Audit Service - Comprehensive audit logging
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.audit_log import AuditLog
from app.core.config import settings
import aiofiles


class AuditService:
    """Service for managing audit logs"""

    STORAGE_PATH = Path(settings.STORAGE_PATH) / "audit_logs"

    @staticmethod
    async def log_action(
        db: AsyncSession,
        user_id: Optional[UUID],
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None
    ) -> AuditLog:
        """
        Log an audit event to both database and file system

        Args:
            db: Database session
            user_id: ID of user performing action
            action: Action performed (e.g., "CREATE", "UPDATE", "DELETE")
            resource_type: Type of resource affected
            resource_id: ID of resource affected
            details: Additional details about the action
            ip_address: IP address of requester
            user_agent: User agent string
            status: Status of action ("success" or "error")
            error_message: Error message if status is "error"

        Returns:
            AuditLog object
        """
        # Create database entry
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            error_message=error_message
        )

        db.add(audit_log)
        await db.commit()
        await db.refresh(audit_log)

        # Write to JSONL file asynchronously
        await AuditService._write_to_file(audit_log)

        return audit_log

    @staticmethod
    async def _write_to_file(audit_log: AuditLog) -> None:
        """Write audit log to daily JSONL file"""
        try:
            # Create directory structure: YYYY/MM/
            now = datetime.utcnow()
            year_dir = AuditService.STORAGE_PATH / str(now.year)
            month_dir = year_dir / f"{now.month:02d}"
            month_dir.mkdir(parents=True, exist_ok=True)

            # File name: audit_YYYY-MM-DD.jsonl
            file_path = month_dir / f"audit_{now.strftime('%Y-%m-%d')}.jsonl"

            # Prepare log entry
            log_entry = {
                "id": str(audit_log.id),
                "user_id": str(audit_log.user_id) if audit_log.user_id else None,
                "action": audit_log.action,
                "resource_type": audit_log.resource_type,
                "resource_id": str(audit_log.resource_id) if audit_log.resource_id else None,
                "details": audit_log.details,
                "ip_address": audit_log.ip_address,
                "user_agent": audit_log.user_agent,
                "status": audit_log.status,
                "error_message": audit_log.error_message,
                "created_at": audit_log.created_at.isoformat()
            }

            # Append to JSONL file
            async with aiofiles.open(file_path, mode='a') as f:
                await f.write(json.dumps(log_entry) + '\n')

        except Exception as e:
            # Log error but don't fail the main operation
            print(f"Failed to write audit log to file: {e}")

    @staticmethod
    async def get_user_activity(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 100
    ) -> list[AuditLog]:
        """Get recent activity for a user"""
        result = await db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_resource_history(
        db: AsyncSession,
        resource_type: str,
        resource_id: UUID,
        limit: int = 100
    ) -> list[AuditLog]:
        """Get audit history for a specific resource"""
        result = await db.execute(
            select(AuditLog)
            .where(
                AuditLog.resource_type == resource_type,
                AuditLog.resource_id == resource_id
            )
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def search_logs(
        db: AsyncSession,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> list[AuditLog]:
        """Search audit logs with filters"""
        query = select(AuditLog)

        # Apply filters
        if action:
            query = query.where(AuditLog.action == action)
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)
        if status:
            query = query.where(AuditLog.status == status)
        if start_date:
            query = query.where(AuditLog.created_at >= start_date)
        if end_date:
            query = query.where(AuditLog.created_at <= end_date)

        query = query.order_by(AuditLog.created_at.desc()).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_statistics(
        db: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get audit log statistics"""
        from sqlalchemy import func

        query = select(
            AuditLog.action,
            AuditLog.status,
            func.count(AuditLog.id).label('count')
        )

        if start_date:
            query = query.where(AuditLog.created_at >= start_date)
        if end_date:
            query = query.where(AuditLog.created_at <= end_date)

        query = query.group_by(AuditLog.action, AuditLog.status)

        result = await db.execute(query)
        rows = result.all()

        statistics = {
            "by_action": {},
            "by_status": {},
            "total": 0
        }

        for row in rows:
            action, status, count = row
            statistics["total"] += count

            # By action
            if action not in statistics["by_action"]:
                statistics["by_action"][action] = 0
            statistics["by_action"][action] += count

            # By status
            if status not in statistics["by_status"]:
                statistics["by_status"][status] = 0
            statistics["by_status"][status] += count

        return statistics

    @staticmethod
    async def cleanup_old_logs(
        db: AsyncSession,
        days_to_keep: int = 90
    ) -> int:
        """Clean up audit logs older than specified days (from database only)"""
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)

        result = await db.execute(
            select(AuditLog).where(AuditLog.created_at < cutoff_date)
        )
        logs_to_delete = result.scalars().all()

        count = len(logs_to_delete)

        for log in logs_to_delete:
            await db.delete(log)

        await db.commit()

        return count
