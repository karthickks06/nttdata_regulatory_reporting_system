"""Workflow endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.user import User
from app.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowExecutionRequest
from app.services.workflow_service import WorkflowService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new workflow"""
    workflow = await WorkflowService.create_workflow(db, workflow_data.model_dump())
    return workflow


@router.get("/")
async def get_workflows(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of workflows"""
    workflows = await WorkflowService.get_workflows(db, skip, limit, status)
    return workflows


@router.get("/{workflow_id}")
async def get_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get workflow by ID"""
    workflow = await WorkflowService.get_workflow(db, workflow_id)

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )

    return workflow


@router.post("/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute workflow"""
    result = await WorkflowService.execute_workflow(db, workflow_id)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Workflow execution failed")
        )

    return result


@router.put("/{workflow_id}/status")
async def update_workflow_status(
    workflow_id: int,
    status: str,
    result_data: dict = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update workflow status"""
    updated = await WorkflowService.update_workflow_status(
        db, workflow_id, status, result_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )

    return updated
