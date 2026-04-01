"""Permission management endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_permission
from app.db.postgres import get_db
from app.models.user import User
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from sqlalchemy import select

router = APIRouter()


@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("admin:write"))
):
    """Create a new permission"""
    new_permission = Permission(**permission_data.model_dump())
    db.add(new_permission)
    await db.commit()
    await db.refresh(new_permission)
    return new_permission


@router.get("/", response_model=List[PermissionResponse])
async def get_permissions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of permissions"""
    result = await db.execute(
        select(Permission).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get permission by ID"""
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    permission = result.scalar_one_or_none()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    return permission


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("admin:write"))
):
    """Delete permission"""
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    permission = result.scalar_one_or_none()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    await db.delete(permission)
    await db.commit()
