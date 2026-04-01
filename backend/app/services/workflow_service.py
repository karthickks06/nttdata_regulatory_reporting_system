"""Workflow orchestration service"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from pathlib import Path

from app.models.workflow import Workflow
from app.core.config import settings


class WorkflowService:
    """Service for workflow management and orchestration"""

    @staticmethod
    async def create_workflow(
        db: AsyncSession,
        workflow_data: dict
    ) -> Workflow:
        """Create a new workflow"""
        new_workflow = Workflow(**workflow_data)
        db.add(new_workflow)
        await db.commit()
        await db.refresh(new_workflow)

        # Save workflow definition to storage
        await WorkflowService._save_workflow_definition(new_workflow)

        return new_workflow

    @staticmethod
    async def get_workflow(
        db: AsyncSession,
        workflow_id: int
    ) -> Optional[Workflow]:
        """Get workflow by ID"""
        result = await db.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_workflows(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Workflow]:
        """Get list of workflows"""
        query = select(Workflow)

        if status:
            query = query.where(Workflow.status == status)

        query = query.order_by(Workflow.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_workflow_status(
        db: AsyncSession,
        workflow_id: int,
        status: str,
        result_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Workflow]:
        """Update workflow status"""
        result = await db.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        workflow = result.scalar_one_or_none()

        if not workflow:
            return None

        workflow.status = status
        workflow.updated_at = datetime.utcnow()

        if status == "completed":
            workflow.completed_at = datetime.utcnow()

        if result_data:
            workflow.result = result_data

        await db.commit()
        await db.refresh(workflow)

        # Save workflow execution state
        await WorkflowService._save_workflow_state(workflow)

        return workflow

    @staticmethod
    async def execute_workflow(
        db: AsyncSession,
        workflow_id: int
    ) -> Dict[str, Any]:
        """
        Execute workflow.

        Args:
            db: Database session
            workflow_id: Workflow ID

        Returns:
            Execution result
        """
        workflow = await WorkflowService.get_workflow(db, workflow_id)

        if not workflow:
            return {
                "success": False,
                "error": "Workflow not found"
            }

        # Update status to running
        await WorkflowService.update_workflow_status(db, workflow_id, "running")

        try:
            # Execute workflow steps
            steps = workflow.workflow_definition.get("steps", [])
            results = []

            for step in steps:
                step_result = await WorkflowService._execute_step(step)
                results.append(step_result)

                if not step_result.get("success"):
                    # Step failed
                    await WorkflowService.update_workflow_status(
                        db,
                        workflow_id,
                        "failed",
                        {"error": step_result.get("error"), "results": results}
                    )
                    return {
                        "success": False,
                        "error": "Workflow step failed",
                        "results": results
                    }

            # All steps successful
            await WorkflowService.update_workflow_status(
                db,
                workflow_id,
                "completed",
                {"results": results}
            )

            return {
                "success": True,
                "results": results
            }

        except Exception as e:
            await WorkflowService.update_workflow_status(
                db,
                workflow_id,
                "failed",
                {"error": str(e)}
            )

            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def _execute_step(step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        # Placeholder implementation
        step_type = step.get("type")
        step_name = step.get("name")

        # This would call appropriate agents/services based on step type
        return {
            "success": True,
            "step_name": step_name,
            "step_type": step_type,
            "executed_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    async def _save_workflow_definition(workflow: Workflow):
        """Save workflow definition to storage"""
        workflow_dir = settings.STORAGE_PATH / "workflows" / "definitions"
        workflow_dir.mkdir(parents=True, exist_ok=True)

        file_path = workflow_dir / f"workflow_{workflow.id}.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                "id": workflow.id,
                "name": workflow.name,
                "workflow_type": workflow.workflow_type,
                "definition": workflow.workflow_definition,
                "created_at": workflow.created_at.isoformat()
            }, f, indent=2)

    @staticmethod
    async def _save_workflow_state(workflow: Workflow):
        """Save workflow execution state"""
        state_dir = settings.STORAGE_PATH / "workflows" / "state"
        state_dir.mkdir(parents=True, exist_ok=True)

        file_path = state_dir / f"workflow_{workflow.id}_state.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                "id": workflow.id,
                "status": workflow.status,
                "result": workflow.result,
                "updated_at": workflow.updated_at.isoformat()
            }, f, indent=2)
