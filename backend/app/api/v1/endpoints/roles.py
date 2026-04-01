"""Role management endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_permission
from app.db.postgres import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from sqlalchemy import select

router = APIRouter()


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("admin:write"))
):
    """Create a new role"""
    new_role = Role(**role_data.model_dump())
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role


@router.get("/", response_model=List[RoleResponse])
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of roles"""
    result = await db.execute(
        select(Role).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get role by ID"""
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    return role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("admin:write"))
):
    """Update role"""
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    update_dict = role_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(role, key, value)

    await db.commit()
    await db.refresh(role)

    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("admin:write"))
):
    """Delete role"""
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    await db.delete(role)
    await db.commit()
