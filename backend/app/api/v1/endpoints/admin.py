"""
Admin API Endpoints - System administration and monitoring
"""
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.services.audit_service import AuditService
from app.services.workflow_storage import WorkflowStorageService
from app.core.rbac import require_permission

router = APIRouter()


@router.get("/system/health")
async def get_system_health(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get system health status"""
    await require_permission(db, current_user.id, "system", "monitor")

    try:
        # Check database connection
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # Check ChromaDB
    try:
        from app.db.chroma_db import get_chroma_client
        chroma_client = get_chroma_client()
        chroma_status = "healthy"
    except Exception as e:
        chroma_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" and chroma_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": db_status,
            "chromadb": chroma_status
        }
    }


@router.get("/system/metrics")
async def get_system_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get system metrics"""
    await require_permission(db, current_user.id, "system", "monitor")

    from sqlalchemy import func, select
    from app.models.user import User
    from app.models.regulatory_update import RegulatoryUpdate
    from app.models.requirement import Requirement
    from app.models.report import Report
    from app.models.workflow import Workflow

    # Count totals
    user_count = await db.scalar(select(func.count(User.id)))
    update_count = await db.scalar(select(func.count(RegulatoryUpdate.id)))
    requirement_count = await db.scalar(select(func.count(Requirement.id)))
    report_count = await db.scalar(select(func.count(Report.id)))
    workflow_count = await db.scalar(select(func.count(Workflow.id)))

    # Active workflows
    active_workflows = await db.scalar(
        select(func.count(Workflow.id))
        .where(Workflow.status.in_(["pending", "in_progress"]))
    )

    # Workflow statistics
    workflow_stats = await WorkflowStorageService.get_workflow_statistics()

    return {
        "users": user_count,
        "regulatory_updates": update_count,
        "requirements": requirement_count,
        "reports": report_count,
        "workflows": {
            "total": workflow_count,
            "active": active_workflows,
            "storage": workflow_stats
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/audit/logs")
async def get_audit_logs(
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    status: Optional[str] = None,
    days: int = 7,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get audit logs with filters"""
    await require_permission(db, current_user.id, "audit_logs", "read")

    start_date = datetime.utcnow() - timedelta(days=days)

    logs = await AuditService.search_logs(
        db=db,
        action=action,
        resource_type=resource_type,
        status=status,
        start_date=start_date,
        limit=limit
    )

    return {
        "logs": [
            {
                "id": str(log.id),
                "user_id": str(log.user_id) if log.user_id else None,
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": str(log.resource_id) if log.resource_id else None,
                "status": log.status,
                "created_at": log.created_at.isoformat(),
                "details": log.details
            }
            for log in logs
        ],
        "count": len(logs)
    }


@router.get("/audit/statistics")
async def get_audit_statistics(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get audit log statistics"""
    await require_permission(db, current_user.id, "audit_logs", "read")

    start_date = datetime.utcnow() - timedelta(days=days)

    stats = await AuditService.get_statistics(
        db=db,
        start_date=start_date
    )

    return stats


@router.post("/audit/cleanup")
async def cleanup_audit_logs(
    days_to_keep: int = 90,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clean up old audit logs from database"""
    await require_permission(db, current_user.id, "system", "admin")

    deleted_count = await AuditService.cleanup_old_logs(
        db=db,
        days_to_keep=days_to_keep
    )

    return {
        "status": "success",
        "deleted_count": deleted_count,
        "days_kept": days_to_keep
    }


@router.post("/workflows/cleanup")
async def cleanup_workflow_history(
    days_to_keep: int = 90,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clean up old workflow history files"""
    await require_permission(db, current_user.id, "system", "admin")

    deleted_count = await WorkflowStorageService.cleanup_old_history(
        days_to_keep=days_to_keep
    )

    return {
        "status": "success",
        "deleted_count": deleted_count,
        "days_kept": days_to_keep
    }


@router.get("/workflows/active")
async def get_active_workflows(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all active workflow executions"""
    await require_permission(db, current_user.id, "workflows", "monitor")

    active = await WorkflowStorageService.get_active_executions()

    return {
        "active_workflows": active,
        "count": len(active)
    }


@router.get("/workflows/history")
async def get_workflow_history(
    year: Optional[int] = None,
    month: Optional[int] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get workflow execution history"""
    await require_permission(db, current_user.id, "workflows", "monitor")

    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    history = await WorkflowStorageService.get_execution_history(
        year=year,
        month=month,
        limit=limit
    )

    return {
        "year": year,
        "month": month,
        "history": history,
        "count": len(history)
    }


@router.get("/cache/stats")
async def get_cache_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get cache statistics"""
    await require_permission(db, current_user.id, "system", "monitor")

    from sqlalchemy import func, select
    from app.models.cache import Cache

    total_entries = await db.scalar(select(func.count(Cache.id)))

    # Count expired entries
    expired_entries = await db.scalar(
        select(func.count(Cache.id))
        .where(Cache.expires_at < datetime.utcnow())
    )

    return {
        "total_entries": total_entries,
        "expired_entries": expired_entries,
        "active_entries": total_entries - expired_entries
    }


@router.post("/cache/clear")
async def clear_cache(
    expired_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clear cache entries"""
    await require_permission(db, current_user.id, "system", "admin")

    from app.models.cache import Cache

    if expired_only:
        result = await db.execute(
            select(Cache).where(Cache.expires_at < datetime.utcnow())
        )
    else:
        result = await db.execute(select(Cache))

    entries_to_delete = result.scalars().all()
    count = len(entries_to_delete)

    for entry in entries_to_delete:
        await db.delete(entry)

    await db.commit()

    return {
        "status": "success",
        "deleted_count": count,
        "expired_only": expired_only
    }


@router.get("/tasks/queue")
async def get_task_queue_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task queue status"""
    await require_permission(db, current_user.id, "system", "monitor")

    from sqlalchemy import func, select
    from app.models.task_queue import TaskQueue

    total_tasks = await db.scalar(select(func.count(TaskQueue.id)))

    # Count by status
    pending = await db.scalar(
        select(func.count(TaskQueue.id))
        .where(TaskQueue.status == "pending")
    )

    running = await db.scalar(
        select(func.count(TaskQueue.id))
        .where(TaskQueue.status == "running")
    )

    completed = await db.scalar(
        select(func.count(TaskQueue.id))
        .where(TaskQueue.status == "completed")
    )

    failed = await db.scalar(
        select(func.count(TaskQueue.id))
        .where(TaskQueue.status == "failed")
    )

    return {
        "total_tasks": total_tasks,
        "by_status": {
            "pending": pending,
            "running": running,
            "completed": completed,
            "failed": failed
        }
    }
