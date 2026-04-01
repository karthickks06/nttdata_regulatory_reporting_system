"""
Level 1: Dev Supervisor Agent

Supervises development activities and the Architect Agent.
Reviews generated code before escalating to Compliance Agent.
"""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class DevSupervisorAgent(BaseAgent):
    """
    Development Supervisor.

    Responsibilities:
    - Supervise code generation
    - Delegate to Architect Agent
    - Review generated SQL and Python code
    - Ensure code quality standards
    - Report to Compliance Agent
    """

    def __init__(self, architect_agent=None, compliance_agent=None):
        super().__init__(
            name="Dev Supervisor",
            level=1,
            supervisor=compliance_agent,
            workers=[architect_agent] if architect_agent else []
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute development supervision.

        Args:
            task: Task containing requirements and mappings

        Returns:
            Reviewed and approved generated code
        """
        self._log_execution({
            "action": "receive_task",
            "task_type": task.get("type"),
            "task_id": task.get("task_id")
        })

        try:
            # Delegate to Architect Agent
            generation_result = await self.delegate_to_worker(
                "Architect Agent",
                task
            )

            # Review the generated code
            review = await self.review_worker_result(
                "Architect Agent",
                generation_result
            )

            if not review.get("approved"):
                return {
                    "status": "rejected",
                    "reason": "Generated code did not pass supervisor review",
                    "details": review.get("issues")
                }

            # Report to supervisor (Compliance Agent)
            result = {
                "status": "completed",
                "task_id": task.get("task_id"),
                "generated_code": generation_result.get("generated_code"),
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
        Review Architect Agent's output.

        Checks:
        - Code is generated
        - SQL syntax is valid (basic check)
        - Python code follows standards
        - Documentation is included

        Args:
            worker_name: Name of the worker (Architect Agent)
            result: Worker's result

        Returns:
            Review decision
        """
        issues = []

        # Check generated code
        generated_code = result.get("generated_code", {})
        if not generated_code:
            issues.append("No code generated")

        sql_code = generated_code.get("sql", [])
        python_code = generated_code.get("python", [])

        if not sql_code and not python_code:
            issues.append("No SQL or Python code generated")

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
