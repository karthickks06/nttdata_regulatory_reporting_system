"""Regulatory updates service for CRUD operations"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from app.models.regulatory_update import RegulatoryUpdate, RegulatorySource
from app.schemas.regulatory_update import RegulatoryUpdateCreate, RegulatoryUpdateUpdate


class RegulatoryService:
    """Service for regulatory updates operations"""

    @staticmethod
    async def create_regulatory_update(
        db: AsyncSession,
        regulatory_data: RegulatoryUpdateCreate
    ) -> RegulatoryUpdate:
        """
        Create a new regulatory update.

        Args:
            db: Database session
            regulatory_data: Regulatory update data

        Returns:
            Created regulatory update
        """
        new_update = RegulatoryUpdate(
            **regulatory_data.model_dump()
        )

        db.add(new_update)
        await db.commit()
        await db.refresh(new_update)

        return new_update

    @staticmethod
    async def get_regulatory_update(
        db: AsyncSession,
        update_id: int
    ) -> Optional[RegulatoryUpdate]:
        """
        Get regulatory update by ID.

        Args:
            db: Database session
            update_id: Regulatory update ID

        Returns:
            Regulatory update or None
        """
        result = await db.execute(
            select(RegulatoryUpdate).where(RegulatoryUpdate.id == update_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_regulatory_updates(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        source: Optional[RegulatorySource] = None,
        is_processed: Optional[bool] = None
    ) -> List[RegulatoryUpdate]:
        """
        Get list of regulatory updates with filters.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records
            source: Filter by regulatory source
            is_processed: Filter by processed status

        Returns:
            List of regulatory updates
        """
        query = select(RegulatoryUpdate)

        if source:
            query = query.where(RegulatoryUpdate.source == source)

        if is_processed is not None:
            query = query.where(RegulatoryUpdate.is_processed == is_processed)

        query = query.order_by(RegulatoryUpdate.published_date.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_regulatory_update(
        db: AsyncSession,
        update_id: int,
        update_data: RegulatoryUpdateUpdate
    ) -> Optional[RegulatoryUpdate]:
        """
        Update regulatory update.

        Args:
            db: Database session
            update_id: Regulatory update ID
            update_data: Update data

        Returns:
            Updated regulatory update or None
        """
        result = await db.execute(
            select(RegulatoryUpdate).where(RegulatoryUpdate.id == update_id)
        )
        regulatory_update = result.scalar_one_or_none()

        if not regulatory_update:
            return None

        # Update fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(regulatory_update, key, value)

        regulatory_update.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(regulatory_update)

        return regulatory_update

    @staticmethod
    async def delete_regulatory_update(
        db: AsyncSession,
        update_id: int
    ) -> bool:
        """
        Delete regulatory update.

        Args:
            db: Database session
            update_id: Regulatory update ID

        Returns:
            True if deleted, False otherwise
        """
        result = await db.execute(
            select(RegulatoryUpdate).where(RegulatoryUpdate.id == update_id)
        )
        regulatory_update = result.scalar_one_or_none()

        if not regulatory_update:
            return False

        await db.delete(regulatory_update)
        await db.commit()

        return True

    @staticmethod
    async def mark_as_processed(
        db: AsyncSession,
        update_id: int
    ) -> Optional[RegulatoryUpdate]:
        """
        Mark regulatory update as processed.

        Args:
            db: Database session
            update_id: Regulatory update ID

        Returns:
            Updated regulatory update or None
        """
        result = await db.execute(
            select(RegulatoryUpdate).where(RegulatoryUpdate.id == update_id)
        )
        regulatory_update = result.scalar_one_or_none()

        if not regulatory_update:
            return None

        regulatory_update.is_processed = True
        regulatory_update.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(regulatory_update)

        return regulatory_update

    @staticmethod
    async def get_by_reference_number(
        db: AsyncSession,
        reference_number: str
    ) -> Optional[RegulatoryUpdate]:
        """
        Get regulatory update by reference number.

        Args:
            db: Database session
            reference_number: Reference number

        Returns:
            Regulatory update or None
        """
        result = await db.execute(
            select(RegulatoryUpdate).where(
                RegulatoryUpdate.reference_number == reference_number
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def search_regulatory_updates(
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[RegulatoryUpdate]:
        """
        Search regulatory updates by title or description.

        Args:
            db: Database session
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records

        Returns:
            List of matching regulatory updates
        """
        search_pattern = f"%{search_term}%"

        query = select(RegulatoryUpdate).where(
            (RegulatoryUpdate.title.ilike(search_pattern)) |
            (RegulatoryUpdate.description.ilike(search_pattern))
        )

        query = query.order_by(RegulatoryUpdate.published_date.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_statistics(
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Get regulatory updates statistics.

        Args:
            db: Database session

        Returns:
            Statistics dictionary
        """
        # Total count
        total_result = await db.execute(
            select(func.count()).select_from(RegulatoryUpdate)
        )
        total = total_result.scalar()

        # Processed count
        processed_result = await db.execute(
            select(func.count()).select_from(RegulatoryUpdate).where(
                RegulatoryUpdate.is_processed == True
            )
        )
        processed = processed_result.scalar()

        # By source
        source_result = await db.execute(
            select(
                RegulatoryUpdate.source,
                func.count(RegulatoryUpdate.id)
            ).group_by(RegulatoryUpdate.source)
        )
        by_source = {source: count for source, count in source_result.all()}

        return {
            "total": total,
            "processed": processed,
            "pending": total - processed,
            "by_source": by_source
        }
