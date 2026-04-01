"""
Level 1: QA Supervisor Agent

Supervises quality assurance activities and the Auditor Agent.
Reviews test results and validation before escalating to Compliance Agent.
"""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class QASupervisorAgent(BaseAgent):
    """
    Quality Assurance Supervisor.

    Responsibilities:
    - Supervise code validation
    - Delegate to Auditor Agent
    - Review test results
    - Ensure compliance validation
    - Report to Compliance Agent
    """

    def __init__(self, auditor_agent=None, compliance_agent=None):
        super().__init__(
            name="QA Supervisor",
            level=1,
            supervisor=compliance_agent,
            workers=[auditor_agent] if auditor_agent else []
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute QA supervision.

        Args:
            task: Task containing code to validate

        Returns:
            Reviewed and approved validation results
        """
        self._log_execution({
            "action": "receive_task",
            "task_type": task.get("type"),
            "task_id": task.get("task_id")
        })

        try:
            # Delegate to Auditor Agent
            validation_result = await self.delegate_to_worker(
                "Auditor Agent",
                task
            )

            # Review the validation results
            review = await self.review_worker_result(
                "Auditor Agent",
                validation_result
            )

            if not review.get("approved"):
                return {
                    "status": "rejected",
                    "reason": "Validation did not pass supervisor review",
                    "details": review.get("issues")
                }

            # Report to supervisor (Compliance Agent)
            result = {
                "status": "completed",
                "task_id": task.get("task_id"),
                "validation_results": validation_result.get("validation_results"),
                "test_results": validation_result.get("test_results"),
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
        Review Auditor Agent's output.

        Checks:
        - All tests passed
        - Validation rules satisfied
        - Compliance requirements met
        - No critical issues found

        Args:
            worker_name: Name of the worker (Auditor Agent)
            result: Worker's result

        Returns:
            Review decision
        """
        issues = []

        # Check validation results
        validation_results = result.get("validation_results", {})
        if not validation_results:
            issues.append("No validation results")

        # Check test results
        test_results = result.get("test_results", {})
        tests_passed = test_results.get("passed", 0)
        tests_failed = test_results.get("failed", 0)

        if tests_failed > 0:
            issues.append(f"{tests_failed} tests failed")

        # Check compliance
        compliance_check = validation_results.get("compliance_met", False)
        if not compliance_check:
            issues.append("Compliance requirements not met")

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
