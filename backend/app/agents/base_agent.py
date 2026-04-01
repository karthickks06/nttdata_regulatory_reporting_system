"""Base agent class for all MCP agents"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from datetime import datetime
import json


class BaseAgent(ABC):
    """
    Base class for all agents in the hierarchical structure.

    Attributes:
        name: Agent name
        level: Hierarchy level (0=master, 1=supervisor, 2=worker)
        supervisor: Reference to supervisor agent (if any)
        workers: List of worker agents (if any)
    """

    def __init__(
        self,
        name: str,
        level: int,
        supervisor: Optional['BaseAgent'] = None,
        workers: Optional[List['BaseAgent']] = None
    ):
        self.name = name
        self.level = level
        self.supervisor = supervisor
        self.workers = workers or []
        self.execution_history: List[Dict[str, Any]] = []

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.

        Args:
            task: Task data containing input and parameters

        Returns:
            Task result with status and output data
        """
        pass

    async def delegate_to_worker(
        self,
        worker_name: str,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Delegate a task to a worker agent.

        Args:
            worker_name: Name of the worker agent
            task: Task data to delegate

        Returns:
            Worker's task result
        """
        worker = next((w for w in self.workers if w.name == worker_name), None)

        if not worker:
            raise ValueError(f"Worker '{worker_name}' not found")

        # Add delegation metadata
        task["delegated_by"] = self.name
        task["delegation_time"] = datetime.utcnow().isoformat()

        # Execute worker task
        result = await worker.execute(task)

        # Log delegation in history
        self._log_execution({
            "action": "delegation",
            "worker": worker_name,
            "task_id": task.get("task_id"),
            "result_status": result.get("status")
        })

        return result

    async def report_to_supervisor(
        self,
        result: Dict[str, Any]
    ) -> None:
        """
        Report task result to supervisor.

        Args:
            result: Task execution result
        """
        if self.supervisor:
            result["reported_by"] = self.name
            result["report_time"] = datetime.utcnow().isoformat()
            # Supervisor can review and approve/reject
            await self.supervisor.review_worker_result(self.name, result)

    async def review_worker_result(
        self,
        worker_name: str,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Review result from a worker agent.

        Args:
            worker_name: Name of the worker
            result: Worker's result

        Returns:
            Review decision (approved/rejected)
        """
        # Default implementation - can be overridden
        self._log_execution({
            "action": "review",
            "worker": worker_name,
            "status": result.get("status"),
            "approved": True
        })

        return {
            "approved": True,
            "reviewed_by": self.name,
            "review_time": datetime.utcnow().isoformat()
        }

    def _log_execution(self, log_entry: Dict[str, Any]) -> None:
        """
        Log execution activity.

        Args:
            log_entry: Log entry data
        """
        log_entry["timestamp"] = datetime.utcnow().isoformat()
        log_entry["agent"] = self.name
        log_entry["level"] = self.level
        self.execution_history.append(log_entry)

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get agent's execution history"""
        return self.execution_history

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', level={self.level})>"
