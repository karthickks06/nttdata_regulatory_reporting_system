"""Task queue worker for executing agent tasks"""

import asyncio
import json
from datetime import datetime
from sqlalchemy import text
from app.db.postgres import engine
from app.models.task_queue import TaskStatus


class TaskQueueWorker:
    """Worker that processes tasks from the task queue"""

    def __init__(self):
        self.running = False

    async def run(self):
        """Run the task queue worker loop"""
        self.running = True

        while self.running:
            try:
                await self.process_next_task()
                await asyncio.sleep(5)  # Check for new tasks every 5 seconds
            except Exception as e:
                print(f"❌ Task worker error: {e}")
                await asyncio.sleep(10)

    async def process_next_task(self):
        """Fetch and process the next pending task"""

        async with engine.begin() as conn:
            # Get next pending task (highest priority first)
            result = await conn.execute(
                text("""
                    SELECT id, task_id, agent_type, task_type, input_data, retry_count
                    FROM task_queue
                    WHERE status = :status
                    ORDER BY priority DESC, created_at ASC
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                """),
                {"status": TaskStatus.PENDING.value}
            )

            row = result.fetchone()

            if not row:
                return  # No pending tasks

            task_id, task_uuid, agent_type, task_type, input_data, retry_count = row

            # Mark task as running
            await conn.execute(
                text("""
                    UPDATE task_queue
                    SET status = :status, started_at = :started_at
                    WHERE id = :id
                """),
                {
                    "status": TaskStatus.RUNNING.value,
                    "started_at": datetime.utcnow(),
                    "id": task_id
                }
            )

            await conn.commit()

        # Execute task outside the transaction
        try:
            print(f"🤖 Processing task {task_uuid} ({agent_type}/{task_type})")

            # Parse input data
            input_dict = json.loads(input_data)

            # Execute the agent task (to be implemented)
            result_data = await self.execute_agent_task(
                agent_type, task_type, input_dict
            )

            # Mark task as completed
            async with engine.begin() as conn:
                await conn.execute(
                    text("""
                        UPDATE task_queue
                        SET status = :status, result_data = :result_data,
                            completed_at = :completed_at
                        WHERE id = :id
                    """),
                    {
                        "status": TaskStatus.COMPLETED.value,
                        "result_data": json.dumps(result_data),
                        "completed_at": datetime.utcnow(),
                        "id": task_id
                    }
                )

            print(f"✅ Task {task_uuid} completed")

        except Exception as e:
            # Mark task as failed
            async with engine.begin() as conn:
                await conn.execute(
                    text("""
                        UPDATE task_queue
                        SET status = :status, error_message = :error_message,
                            completed_at = :completed_at, retry_count = :retry_count
                        WHERE id = :id
                    """),
                    {
                        "status": TaskStatus.FAILED.value,
                        "error_message": str(e),
                        "completed_at": datetime.utcnow(),
                        "retry_count": retry_count + 1,
                        "id": task_id
                    }
                )

            print(f"❌ Task {task_uuid} failed: {e}")

    async def execute_agent_task(self, agent_type: str, task_type: str, input_data: dict) -> dict:
        """
        Execute an agent task.

        This is a placeholder that will be implemented with actual agent logic.

        Args:
            agent_type: Type of agent to execute
            task_type: Type of task to perform
            input_data: Input data for the task

        Returns:
            Result data from the agent execution
        """
        # Simulate task execution
        await asyncio.sleep(2)

        return {
            "status": "success",
            "message": f"Task {task_type} executed by {agent_type}",
            "timestamp": datetime.utcnow().isoformat()
        }

    def stop(self):
        """Stop the task queue worker"""
        self.running = False
