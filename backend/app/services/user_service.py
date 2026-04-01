"""User management service"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.role import Role
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for user management operations"""

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.username == username)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get list of users"""
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(user_data.password)

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            department=user_data.department
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        user_data: UserUpdate
    ) -> Optional[User]:
        """Update user information"""
        user = await UserService.get_user_by_id(db, user_id)

        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """Delete a user"""
        user = await UserService.get_user_by_id(db, user_id)

        if not user:
            return False

        await db.delete(user)
        await db.commit()

        return True

    @staticmethod
    async def assign_role(
        db: AsyncSession,
        user_id: int,
        role_id: int
    ) -> bool:
        """Assign a role to a user"""
        user = await UserService.get_user_by_id(db, user_id)
        result = await db.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()

        if not user or not role:
            return False

        if role not in user.roles:
            user.roles.append(role)
            await db.commit()

        return True

    @staticmethod
    async def remove_role(
        db: AsyncSession,
        user_id: int,
        role_id: int
    ) -> bool:
        """Remove a role from a user"""
        user = await UserService.get_user_by_id(db, user_id)
        result = await db.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()

        if not user or not role:
            return False

        if role in user.roles:
            user.roles.remove(role)
            await db.commit()

        return True
