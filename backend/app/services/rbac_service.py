"""
RBAC Service - Role-Based Access Control Business Logic
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.core.exceptions import NotFoundException, ForbiddenException


class RBACService:
    """Service for managing Role-Based Access Control"""

    @staticmethod
    async def get_user_roles(db: AsyncSession, user_id: UUID) -> List[Role]:
        """Get all roles assigned to a user"""
        result = await db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.roles))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException(f"User {user_id} not found")

        return user.roles

    @staticmethod
    async def get_user_permissions(db: AsyncSession, user_id: UUID) -> List[Permission]:
        """Get all permissions for a user (through roles)"""
        result = await db.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.roles).selectinload(Role.permissions)
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException(f"User {user_id} not found")

        # Collect unique permissions from all roles
        permissions = set()
        for role in user.roles:
            permissions.update(role.permissions)

        return list(permissions)

    @staticmethod
    async def assign_role_to_user(
        db: AsyncSession,
        user_id: UUID,
        role_id: UUID,
        assigned_by: Optional[UUID] = None
    ) -> bool:
        """Assign a role to a user"""
        # Verify user exists
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        if not user:
            raise NotFoundException(f"User {user_id} not found")

        # Verify role exists
        role_result = await db.execute(select(Role).where(Role.id == role_id))
        role = role_result.scalar_one_or_none()
        if not role:
            raise NotFoundException(f"Role {role_id} not found")

        # Add role to user
        if role not in user.roles:
            user.roles.append(role)
            await db.commit()
            return True

        return False

    @staticmethod
    async def remove_role_from_user(
        db: AsyncSession,
        user_id: UUID,
        role_id: UUID
    ) -> bool:
        """Remove a role from a user"""
        # Get user with roles
        result = await db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.roles))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException(f"User {user_id} not found")

        # Find and remove the role
        role_to_remove = None
        for role in user.roles:
            if role.id == role_id:
                role_to_remove = role
                break

        if role_to_remove:
            user.roles.remove(role_to_remove)
            await db.commit()
            return True

        return False

    @staticmethod
    async def assign_permission_to_role(
        db: AsyncSession,
        role_id: UUID,
        permission_id: UUID
    ) -> bool:
        """Assign a permission to a role"""
        # Get role with permissions
        result = await db.execute(
            select(Role)
            .where(Role.id == role_id)
            .options(selectinload(Role.permissions))
        )
        role = result.scalar_one_or_none()

        if not role:
            raise NotFoundException(f"Role {role_id} not found")

        # Get permission
        perm_result = await db.execute(
            select(Permission).where(Permission.id == permission_id)
        )
        permission = perm_result.scalar_one_or_none()

        if not permission:
            raise NotFoundException(f"Permission {permission_id} not found")

        # Add permission to role
        if permission not in role.permissions:
            role.permissions.append(permission)
            await db.commit()
            return True

        return False

    @staticmethod
    async def remove_permission_from_role(
        db: AsyncSession,
        role_id: UUID,
        permission_id: UUID
    ) -> bool:
        """Remove a permission from a role"""
        # Get role with permissions
        result = await db.execute(
            select(Role)
            .where(Role.id == role_id)
            .options(selectinload(Role.permissions))
        )
        role = result.scalar_one_or_none()

        if not role:
            raise NotFoundException(f"Role {role_id} not found")

        # Find and remove the permission
        perm_to_remove = None
        for perm in role.permissions:
            if perm.id == permission_id:
                perm_to_remove = perm
                break

        if perm_to_remove:
            role.permissions.remove(perm_to_remove)
            await db.commit()
            return True

        return False

    @staticmethod
    async def check_permission(
        db: AsyncSession,
        user_id: UUID,
        resource: str,
        action: str
    ) -> bool:
        """Check if user has specific permission"""
        permissions = await RBACService.get_user_permissions(db, user_id)

        # Check for superuser (has all permissions)
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        if user and user.is_superuser:
            return True

        # Check permissions
        for perm in permissions:
            if perm.resource == resource and perm.action == action:
                return True

        return False

    @staticmethod
    async def require_permission(
        db: AsyncSession,
        user_id: UUID,
        resource: str,
        action: str
    ) -> None:
        """Require permission or raise exception"""
        has_permission = await RBACService.check_permission(
            db, user_id, resource, action
        )

        if not has_permission:
            raise ForbiddenException(
                f"User does not have permission to {action} on {resource}"
            )

    @staticmethod
    async def get_role_by_name(db: AsyncSession, role_name: str) -> Optional[Role]:
        """Get role by name"""
        result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_permission_by_name(
        db: AsyncSession,
        permission_name: str
    ) -> Optional[Permission]:
        """Get permission by name"""
        result = await db.execute(
            select(Permission).where(Permission.name == permission_name)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_all_roles(db: AsyncSession) -> List[Role]:
        """List all roles"""
        result = await db.execute(select(Role))
        return list(result.scalars().all())

    @staticmethod
    async def list_all_permissions(db: AsyncSession) -> List[Permission]:
        """List all permissions"""
        result = await db.execute(select(Permission))
        return list(result.scalars().all())
