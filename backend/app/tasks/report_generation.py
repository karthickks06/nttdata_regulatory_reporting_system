"""Report generation background task"""

import asyncio
from typing import Dict, Any
from pathlib import Path

from app.services.report_service import ReportService
from app.db.postgres import AsyncSessionLocal

async def generate_report(report_id: int) -> Dict[str, Any]:
    """
    Generate a report in background.
    
    Args:
        report_id: ID of report to generate
        
    Returns:
        Generation results
    """
    async with AsyncSessionLocal() as db:
        service = ReportService()
        result = await service.generate_report_file(db, report_id)
        return result
