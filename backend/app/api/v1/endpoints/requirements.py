"""Requirements endpoints"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.user import User
from app.services.requirement_service import RequirementService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_requirement(
    requirement_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new requirement"""
    requirement = await RequirementService.create_requirement(db, requirement_data)
    return requirement


@router.get("/")
async def get_requirements(
    skip: int = 0,
    limit: int = 100,
    regulatory_update_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of requirements"""
    requirements = await RequirementService.get_requirements(
        db, skip, limit, regulatory_update_id, status
    )
    return requirements


@router.get("/{requirement_id}")
async def get_requirement(
    requirement_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get requirement by ID"""
    requirement = await RequirementService.get_requirement(db, requirement_id)

    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )

    return requirement


@router.put("/{requirement_id}")
async def update_requirement(
    requirement_id: int,
    update_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update requirement"""
    updated = await RequirementService.update_requirement(db, requirement_id, update_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )

    return updated


@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_requirement(
    requirement_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete requirement"""
    deleted = await RequirementService.delete_requirement(db, requirement_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
