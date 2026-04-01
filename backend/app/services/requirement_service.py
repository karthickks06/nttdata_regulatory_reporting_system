"""Requirements service for CRUD operations"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.requirement import Requirement


class RequirementService:
    """Service for requirements operations"""

    @staticmethod
    async def create_requirement(
        db: AsyncSession,
        requirement_data: dict
    ) -> Requirement:
        """Create a new requirement"""
        new_requirement = Requirement(**requirement_data)
        db.add(new_requirement)
        await db.commit()
        await db.refresh(new_requirement)
        return new_requirement

    @staticmethod
    async def get_requirement(
        db: AsyncSession,
        requirement_id: int
    ) -> Optional[Requirement]:
        """Get requirement by ID"""
        result = await db.execute(
            select(Requirement).where(Requirement.id == requirement_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_requirements(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        regulatory_update_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Requirement]:
        """Get list of requirements with filters"""
        query = select(Requirement)

        if regulatory_update_id:
            query = query.where(Requirement.regulatory_update_id == regulatory_update_id)

        if status:
            query = query.where(Requirement.status == status)

        query = query.order_by(Requirement.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_requirement(
        db: AsyncSession,
        requirement_id: int,
        update_data: dict
    ) -> Optional[Requirement]:
        """Update requirement"""
        result = await db.execute(
            select(Requirement).where(Requirement.id == requirement_id)
        )
        requirement = result.scalar_one_or_none()

        if not requirement:
            return None

        for key, value in update_data.items():
            if value is not None:
                setattr(requirement, key, value)

        requirement.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(requirement)

        return requirement

    @staticmethod
    async def delete_requirement(
        db: AsyncSession,
        requirement_id: int
    ) -> bool:
        """Delete requirement"""
        result = await db.execute(
            select(Requirement).where(Requirement.id == requirement_id)
        )
        requirement = result.scalar_one_or_none()

        if not requirement:
            return False

        await db.delete(requirement)
        await db.commit()
        return True

    @staticmethod
    async def get_by_category(
        db: AsyncSession,
        category: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Requirement]:
        """Get requirements by category"""
        query = select(Requirement).where(Requirement.category == category)
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())
