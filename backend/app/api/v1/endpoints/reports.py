"""Reports endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.user import User
from app.schemas.report import ReportCreate, ReportResponse, ReportGenerationRequest
from app.services.report_service import ReportService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new report"""
    report = await ReportService.create_report(db, report_data.model_dump())
    return report


@router.get("/")
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    report_type: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of reports"""
    reports = await ReportService.get_reports(db, skip, limit, report_type)
    return reports


@router.get("/{report_id}")
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get report by ID"""
    report = await ReportService.get_report(db, report_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return report


@router.post("/generate")
async def generate_report(
    request: ReportGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a report"""
    try:
        if request.format == "csv":
            file_path = await ReportService.generate_csv_report(
                data=request.data.get("records", []),
                filename=f"{request.title}.csv"
            )
        elif request.format == "json":
            file_path = await ReportService.generate_json_report(
                data=request.data,
                filename=f"{request.title}.json"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported format: {request.format}"
            )

        # Save report metadata to database
        report = await ReportService.create_report(db, {
            "report_type": request.report_type,
            "title": request.title,
            "file_path": file_path,
            "report_data": request.data
        })

        return {
            "success": True,
            "report_id": report.id,
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete report"""
    deleted = await ReportService.delete_report(db, report_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
