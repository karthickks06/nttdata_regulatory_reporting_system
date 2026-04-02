"""
Validation API Endpoints - Data validation and quality checks
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.services.validation_service import ValidationService

router = APIRouter()


@router.post("/validate/report/{report_id}")
async def validate_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validate a regulatory report"""
    try:
        result = await ValidationService.validate_report(db, report_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/validate/data-mapping/{mapping_id}")
async def validate_data_mapping(
    mapping_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validate a data mapping"""
    try:
        result = await ValidationService.validate_data_mapping(db, mapping_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/validate/code/{code_id}")
async def validate_generated_code(
    code_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validate generated code"""
    try:
        result = await ValidationService.validate_generated_code(db, code_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/validate/report/{report_id}/results")
async def get_validation_results(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get validation results for a report"""
    try:
        results = await ValidationService.get_validation_results(db, report_id)
        return results
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/validate/data-quality")
async def check_data_quality(
    entity_type: str,
    entity_id: UUID,
    rules: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run data quality checks"""
    result = await ValidationService.check_data_quality(
        db=db,
        entity_type=entity_type,
        entity_id=entity_id,
        rules=rules
    )

    return result


@router.post("/validate/completeness")
async def check_completeness(
    entity_type: str,
    entity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check data completeness"""
    result = await ValidationService.check_completeness(
        db=db,
        entity_type=entity_type,
        entity_id=entity_id
    )

    return result


@router.post("/validate/consistency")
async def check_consistency(
    entity_type: str,
    entity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check data consistency"""
    result = await ValidationService.check_consistency(
        db=db,
        entity_type=entity_type,
        entity_id=entity_id
    )

    return result


@router.post("/validate/anomaly-detection")
async def detect_anomalies(
    report_id: UUID,
    threshold: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Detect anomalies in report data"""
    result = await ValidationService.detect_anomalies(
        db=db,
        report_id=report_id,
        threshold=threshold
    )

    return result


@router.get("/validation/rules")
async def list_validation_rules(
    entity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List available validation rules"""
    rules = await ValidationService.list_validation_rules(
        db=db,
        entity_type=entity_type
    )

    return rules


@router.get("/validation/history/{entity_id}")
async def get_validation_history(
    entity_id: UUID,
    entity_type: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get validation history for an entity"""
    history = await ValidationService.get_validation_history(
        db=db,
        entity_id=entity_id,
        entity_type=entity_type,
        limit=limit
    )

    return history
