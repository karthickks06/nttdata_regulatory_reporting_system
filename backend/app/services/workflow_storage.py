"""
Workflow Storage Service - Local filesystem workflow persistence
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import UUID
import aiofiles

from app.core.config import settings


class WorkflowStorageService:
    """Service for managing workflow execution data on local filesystem"""

    STORAGE_PATH = Path(settings.STORAGE_PATH) / "workflows"

    @staticmethod
    def _ensure_directories():
        """Ensure all workflow directories exist"""
        directories = [
            WorkflowStorageService.STORAGE_PATH / "definitions",
            WorkflowStorageService.STORAGE_PATH / "executions",
            WorkflowStorageService.STORAGE_PATH / "state",
            WorkflowStorageService.STORAGE_PATH / "history",
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    async def save_workflow_definition(
        workflow_id: UUID,
        definition: Dict[str, Any]
    ) -> str:
        """Save workflow definition template"""
        WorkflowStorageService._ensure_directories()

        file_path = (
            WorkflowStorageService.STORAGE_PATH /
            "definitions" /
            f"{workflow_id}.json"
        )

        definition_with_meta = {
            "workflow_id": str(workflow_id),
            "created_at": datetime.utcnow().isoformat(),
            "definition": definition
        }

        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(json.dumps(definition_with_meta, indent=2))

        return str(file_path)

    @staticmethod
    async def get_workflow_definition(workflow_id: UUID) -> Optional[Dict[str, Any]]:
        """Load workflow definition"""
        file_path = (
            WorkflowStorageService.STORAGE_PATH /
            "definitions" /
            f"{workflow_id}.json"
        )

        if not file_path.exists():
            return None

        async with aiofiles.open(file_path, mode='r') as f:
            content = await f.read()
            return json.loads(content)

    @staticmethod
    async def save_execution_state(
        execution_id: UUID,
        state: Dict[str, Any]
    ) -> str:
        """Save current workflow execution state"""
        WorkflowStorageService._ensure_directories()

        # Save to state directory (active executions)
        state_path = (
            WorkflowStorageService.STORAGE_PATH /
            "state" /
            f"{execution_id}.json"
        )

        state_with_meta = {
            "execution_id": str(execution_id),
            "updated_at": datetime.utcnow().isoformat(),
            "state": state
        }

        async with aiofiles.open(state_path, mode='w') as f:
            await f.write(json.dumps(state_with_meta, indent=2))

        return str(state_path)

    @staticmethod
    async def get_execution_state(execution_id: UUID) -> Optional[Dict[str, Any]]:
        """Load execution state"""
        state_path = (
            WorkflowStorageService.STORAGE_PATH /
            "state" /
            f"{execution_id}.json"
        )

        if not state_path.exists():
            return None

        async with aiofiles.open(state_path, mode='r') as f:
            content = await f.read()
            return json.loads(content)

    @staticmethod
    async def save_execution_log(
        execution_id: UUID,
        workflow_name: str,
        steps: List[Dict[str, Any]],
        metadata: Dict[str, Any]
    ) -> str:
        """Save workflow execution log"""
        WorkflowStorageService._ensure_directories()

        # Organize by month
        now = datetime.utcnow()
        month_dir = (
            WorkflowStorageService.STORAGE_PATH /
            "executions" /
            str(now.year) /
            f"{now.month:02d}"
        )
        month_dir.mkdir(parents=True, exist_ok=True)

        file_path = month_dir / f"{execution_id}.json"

        log_data = {
            "execution_id": str(execution_id),
            "workflow_name": workflow_name,
            "executed_at": now.isoformat(),
            "steps": steps,
            "metadata": metadata
        }

        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(json.dumps(log_data, indent=2))

        return str(file_path)

    @staticmethod
    async def archive_execution(
        execution_id: UUID,
        final_status: str
    ) -> bool:
        """Move execution from state to history"""
        state_path = (
            WorkflowStorageService.STORAGE_PATH /
            "state" /
            f"{execution_id}.json"
        )

        if not state_path.exists():
            return False

        # Read current state
        async with aiofiles.open(state_path, mode='r') as f:
            content = await f.read()
            state_data = json.loads(content)

        # Add archival metadata
        state_data["archived_at"] = datetime.utcnow().isoformat()
        state_data["final_status"] = final_status

        # Save to history
        now = datetime.utcnow()
        history_dir = (
            WorkflowStorageService.STORAGE_PATH /
            "history" /
            str(now.year) /
            f"{now.month:02d}"
        )
        history_dir.mkdir(parents=True, exist_ok=True)

        history_path = history_dir / f"{execution_id}.json"

        async with aiofiles.open(history_path, mode='w') as f:
            await f.write(json.dumps(state_data, indent=2))

        # Remove from state directory
        state_path.unlink()

        return True

    @staticmethod
    async def get_execution_history(
        year: int,
        month: int,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get workflow execution history for a specific month"""
        history_dir = (
            WorkflowStorageService.STORAGE_PATH /
            "history" /
            str(year) /
            f"{month:02d}"
        )

        if not history_dir.exists():
            return []

        history_files = sorted(
            history_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        if limit:
            history_files = history_files[:limit]

        history_data = []
        for file_path in history_files:
            async with aiofiles.open(file_path, mode='r') as f:
                content = await f.read()
                history_data.append(json.loads(content))

        return history_data

    @staticmethod
    async def get_active_executions() -> List[Dict[str, Any]]:
        """Get all active workflow executions"""
        state_dir = WorkflowStorageService.STORAGE_PATH / "state"

        if not state_dir.exists():
            return []

        state_files = list(state_dir.glob("*.json"))
        active_executions = []

        for file_path in state_files:
            async with aiofiles.open(file_path, mode='r') as f:
                content = await f.read()
                active_executions.append(json.loads(content))

        return active_executions

    @staticmethod
    async def cleanup_old_history(days_to_keep: int = 90) -> int:
        """Clean up old workflow history files"""
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        history_base = WorkflowStorageService.STORAGE_PATH / "history"

        if not history_base.exists():
            return 0

        deleted_count = 0

        for year_dir in history_base.iterdir():
            if not year_dir.is_dir():
                continue

            for month_dir in year_dir.iterdir():
                if not month_dir.is_dir():
                    continue

                for file_path in month_dir.glob("*.json"):
                    # Check file modification time
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff_date:
                        file_path.unlink()
                        deleted_count += 1

                # Remove empty directories
                if not any(month_dir.iterdir()):
                    month_dir.rmdir()

            if not any(year_dir.iterdir()):
                year_dir.rmdir()

        return deleted_count

    @staticmethod
    async def get_workflow_statistics() -> Dict[str, Any]:
        """Get workflow execution statistics"""
        active = await WorkflowStorageService.get_active_executions()

        # Count history files
        history_base = WorkflowStorageService.STORAGE_PATH / "history"
        total_history = 0

        if history_base.exists():
            for year_dir in history_base.iterdir():
                if year_dir.is_dir():
                    for month_dir in year_dir.iterdir():
                        if month_dir.is_dir():
                            total_history += len(list(month_dir.glob("*.json")))

        return {
            "active_executions": len(active),
            "total_history": total_history,
            "storage_path": str(WorkflowStorageService.STORAGE_PATH)
        }
