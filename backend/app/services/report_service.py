"""Report generation service"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import csv
import json
from pathlib import Path

from app.models.report import Report
from app.core.config import settings


class ReportService:
    """Service for report generation and management"""

    @staticmethod
    async def create_report(
        db: AsyncSession,
        report_data: dict
    ) -> Report:
        """Create a new report"""
        new_report = Report(**report_data)
        db.add(new_report)
        await db.commit()
        await db.refresh(new_report)
        return new_report

    @staticmethod
    async def get_report(
        db: AsyncSession,
        report_id: int
    ) -> Optional[Report]:
        """Get report by ID"""
        result = await db.execute(
            select(Report).where(Report.id == report_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_reports(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        report_type: Optional[str] = None
    ) -> List[Report]:
        """Get list of reports"""
        query = select(Report)

        if report_type:
            query = query.where(Report.report_type == report_type)

        query = query.order_by(Report.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def generate_csv_report(
        data: List[Dict[str, Any]],
        filename: str
    ) -> str:
        """
        Generate CSV report.

        Args:
            data: Report data
            filename: Output filename

        Returns:
            File path
        """
        reports_dir = settings.STORAGE_PATH / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        file_path = reports_dir / filename

        if data:
            keys = data[0].keys()

            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)

        return str(file_path)

    @staticmethod
    async def generate_json_report(
        data: Dict[str, Any],
        filename: str
    ) -> str:
        """Generate JSON report"""
        reports_dir = settings.STORAGE_PATH / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        file_path = reports_dir / filename

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

        return str(file_path)

    @staticmethod
    async def delete_report(
        db: AsyncSession,
        report_id: int
    ) -> bool:
        """Delete report"""
        result = await db.execute(
            select(Report).where(Report.id == report_id)
        )
        report = result.scalar_one_or_none()

        if not report:
            return False

        await db.delete(report)
        await db.commit()
        return True
