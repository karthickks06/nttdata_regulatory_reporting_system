"""Regulatory updates endpoints"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.user import User
from app.models.regulatory_update import RegulatorySource
from app.schemas.regulatory_update import RegulatoryUpdateCreate, RegulatoryUpdateUpdate, RegulatoryUpdateResponse
from app.services.regulatory_service import RegulatoryService

router = APIRouter()


@router.post("/", response_model=RegulatoryUpdateResponse, status_code=status.HTTP_201_CREATED)
async def create_regulatory_update(
    regulatory_data: RegulatoryUpdateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new regulatory update"""
    regulatory_update = await RegulatoryService.create_regulatory_update(db, regulatory_data)
    return regulatory_update


@router.get("/", response_model=List[RegulatoryUpdateResponse])
async def get_regulatory_updates(
    skip: int = 0,
    limit: int = 100,
    source: Optional[RegulatorySource] = None,
    is_processed: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of regulatory updates"""
    updates = await RegulatoryService.get_regulatory_updates(
        db, skip, limit, source, is_processed
    )
    return updates


@router.get("/{update_id}", response_model=RegulatoryUpdateResponse)
async def get_regulatory_update(
    update_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get regulatory update by ID"""
    update = await RegulatoryService.get_regulatory_update(db, update_id)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulatory update not found"
        )

    return update


@router.put("/{update_id}", response_model=RegulatoryUpdateResponse)
async def update_regulatory_update(
    update_id: int,
    update_data: RegulatoryUpdateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update regulatory update"""
    updated = await RegulatoryService.update_regulatory_update(db, update_id, update_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulatory update not found"
        )

    return updated


@router.delete("/{update_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_regulatory_update(
    update_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete regulatory update"""
    deleted = await RegulatoryService.delete_regulatory_update(db, update_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulatory update not found"
        )


@router.post("/{update_id}/mark-processed", response_model=RegulatoryUpdateResponse)
async def mark_as_processed(
    update_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark regulatory update as processed"""
    updated = await RegulatoryService.mark_as_processed(db, update_id)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulatory update not found"
        )

    return updated


@router.get("/search/", response_model=List[RegulatoryUpdateResponse])
async def search_regulatory_updates(
    q: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search regulatory updates"""
    results = await RegulatoryService.search_regulatory_updates(db, q, skip, limit)
    return results


@router.get("/statistics/summary")
async def get_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get regulatory updates statistics"""
    stats = await RegulatoryService.get_statistics(db)
    return stats
