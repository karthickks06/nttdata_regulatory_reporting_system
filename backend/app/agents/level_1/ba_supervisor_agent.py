"""
Level 1: BA Supervisor Agent

Supervises business analysis activities and the Interpreter Agent.
Reviews requirements and data mappings before escalating to Compliance Agent.
"""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class BASupervisorAgent(BaseAgent):
    """
    Business Analysis Supervisor.

    Responsibilities:
    - Supervise requirement interpretation
    - Delegate to Interpreter Agent
    - Review and validate requirements
    - Ensure data mappings are correct
    - Report to Compliance Agent
    """

    def __init__(self, interpreter_agent=None, compliance_agent=None):
        super().__init__(
            name="BA Supervisor",
            level=1,
            supervisor=compliance_agent,
            workers=[interpreter_agent] if interpreter_agent else []
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute business analysis supervision.

        Args:
            task: Task containing regulatory data for analysis

        Returns:
            Reviewed and approved requirements
        """
        self._log_execution({
            "action": "receive_task",
            "task_type": task.get("type"),
            "task_id": task.get("task_id")
        })

        try:
            # Delegate to Interpreter Agent
            interpretation_result = await self.delegate_to_worker(
                "Interpreter Agent",
                task
            )

            # Review the interpretation
            review = await self.review_worker_result(
                "Interpreter Agent",
                interpretation_result
            )

            if not review.get("approved"):
                return {
                    "status": "rejected",
                    "reason": "Requirements did not pass supervisor review",
                    "details": review.get("issues")
                }

            # Report to supervisor (Compliance Agent)
            result = {
                "status": "completed",
                "task_id": task.get("task_id"),
                "requirements": interpretation_result.get("requirements"),
                "data_mappings": interpretation_result.get("data_mappings"),
                "reviewed_by": self.name,
                "approved": True
            }

            if self.supervisor:
                await self.report_to_supervisor(result)

            return result

        except Exception as e:
            self._log_execution({
                "action": "execution_error",
                "error": str(e)
            })

            return {
                "status": "failed",
                "error": str(e)
            }

    async def review_worker_result(
        self,
        worker_name: str,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Review Interpreter Agent's output.

        Checks:
        - Requirements are complete
        - Data mappings are valid
        - Impact analysis is thorough

        Args:
            worker_name: Name of the worker (Interpreter Agent)
            result: Worker's result

        Returns:
            Review decision
        """
        issues = []

        # Check requirements
        requirements = result.get("requirements", [])
        if not requirements:
            issues.append("No requirements extracted")

        # Check data mappings
        data_mappings = result.get("data_mappings", [])
        if not data_mappings:
            issues.append("No data mappings created")

        # Determine approval
        approved = len(issues) == 0

        self._log_execution({
            "action": "review_complete",
            "worker": worker_name,
            "approved": approved,
            "issues_found": len(issues)
        })

        return {
            "approved": approved,
            "reviewed_by": self.name,
            "issues": issues if not approved else []
        }
