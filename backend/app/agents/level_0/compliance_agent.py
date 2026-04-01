"""
Level 0: Compliance Agent - Master Orchestrator

The top-level agent that coordinates all regulatory compliance workflows.
Delegates tasks to supervisors and ensures compliance requirements are met.
"""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class ComplianceAgent(BaseAgent):
    """
    Master orchestrator for regulatory compliance automation.

    Responsibilities:
    - Receive regulatory updates and requirements
    - Orchestrate end-to-end compliance workflow
    - Delegate to BA, Dev, and QA supervisors
    - Ensure quality gates are met
    - Provide final approval
    """

    def __init__(self, supervisors: list = None):
        super().__init__(
            name="Compliance Agent",
            level=0,
            supervisor=None,
            workers=supervisors or []
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute compliance workflow orchestration.

        Workflow:
        1. Analyze regulatory update
        2. Delegate to BA Supervisor for requirement analysis
        3. Delegate to Dev Supervisor for implementation
        4. Delegate to QA Supervisor for validation
        5. Approve and finalize

        Args:
            task: Task containing regulatory update data

        Returns:
            Complete workflow result
        """
        task_type = task.get("type", "compliance_workflow")
        self._log_execution({
            "action": "start_workflow",
            "task_type": task_type,
            "task_id": task.get("task_id")
        })

        try:
            # Phase 1: Business Analysis
            ba_result = await self.delegate_to_worker(
                "BA Supervisor",
                {
                    "task_id": task.get("task_id"),
                    "type": "requirement_analysis",
                    "data": task.get("data")
                }
            )

            if ba_result.get("status") != "completed":
                return {
                    "status": "failed",
                    "phase": "business_analysis",
                    "error": ba_result.get("error")
                }

            # Phase 2: Development
            dev_result = await self.delegate_to_worker(
                "Dev Supervisor",
                {
                    "task_id": task.get("task_id"),
                    "type": "code_generation",
                    "requirements": ba_result.get("requirements"),
                    "mappings": ba_result.get("data_mappings")
                }
            )

            if dev_result.get("status") != "completed":
                return {
                    "status": "failed",
                    "phase": "development",
                    "error": dev_result.get("error")
                }

            # Phase 3: Quality Assurance
            qa_result = await self.delegate_to_worker(
                "QA Supervisor",
                {
                    "task_id": task.get("task_id"),
                    "type": "validation",
                    "generated_code": dev_result.get("generated_code"),
                    "requirements": ba_result.get("requirements")
                }
            )

            if qa_result.get("status") != "completed":
                return {
                    "status": "failed",
                    "phase": "quality_assurance",
                    "error": qa_result.get("error")
                }

            # Final approval
            self._log_execution({
                "action": "approve_workflow",
                "task_id": task.get("task_id"),
                "all_phases": "completed"
            })

            return {
                "status": "completed",
                "task_id": task.get("task_id"),
                "phases": {
                    "business_analysis": ba_result,
                    "development": dev_result,
                    "quality_assurance": qa_result
                },
                "approved_by": self.name,
                "message": "Compliance workflow completed successfully"
            }

        except Exception as e:
            self._log_execution({
                "action": "workflow_error",
                "task_id": task.get("task_id"),
                "error": str(e)
            })

            return {
                "status": "failed",
                "task_id": task.get("task_id"),
                "error": str(e)
            }
