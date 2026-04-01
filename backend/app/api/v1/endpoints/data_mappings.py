"""Data mappings endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.user import User
from app.models.data_mapping import DataMapping
from app.schemas.data_mapping import DataMappingCreate, DataMappingUpdate, DataMappingResponse

router = APIRouter()


@router.post("/", response_model=DataMappingResponse, status_code=status.HTTP_201_CREATED)
async def create_data_mapping(
    mapping_data: DataMappingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new data mapping"""
    new_mapping = DataMapping(**mapping_data.model_dump())
    db.add(new_mapping)
    await db.commit()
    await db.refresh(new_mapping)
    return new_mapping


@router.get("/", response_model=List[DataMappingResponse])
async def get_data_mappings(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of data mappings"""
    result = await db.execute(
        select(DataMapping).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


@router.get("/{mapping_id}", response_model=DataMappingResponse)
async def get_data_mapping(
    mapping_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get data mapping by ID"""
    result = await db.execute(
        select(DataMapping).where(DataMapping.id == mapping_id)
    )
    mapping = result.scalar_one_or_none()

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data mapping not found"
        )

    return mapping


@router.put("/{mapping_id}", response_model=DataMappingResponse)
async def update_data_mapping(
    mapping_id: int,
    mapping_data: DataMappingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update data mapping"""
    result = await db.execute(
        select(DataMapping).where(DataMapping.id == mapping_id)
    )
    mapping = result.scalar_one_or_none()

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data mapping not found"
        )

    update_dict = mapping_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(mapping, key, value)

    await db.commit()
    await db.refresh(mapping)

    return mapping


@router.delete("/{mapping_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_mapping(
    mapping_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete data mapping"""
    result = await db.execute(
        select(DataMapping).where(DataMapping.id == mapping_id)
    )
    mapping = result.scalar_one_or_none()

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data mapping not found"
        )

    await db.delete(mapping)
    await db.commit()
