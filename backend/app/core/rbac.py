"""Role-Based Access Control (RBAC) implementation"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


class RBACService:
    """Service for role-based access control operations"""

    @staticmethod
    async def user_has_permission(
        db: AsyncSession,
        user: User,
        permission_name: str
    ) -> bool:
        """
        Check if user has a specific permission.

        Args:
            db: Database session
            user: User object
            permission_name: Permission name to check

        Returns:
            True if user has permission, False otherwise
        """
        # Superusers have all permissions
        if user.is_superuser:
            return True

        # Check user's roles for the permission
        for role in user.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True

        return False

    @staticmethod
    async def user_has_any_permission(
        db: AsyncSession,
        user: User,
        permission_names: List[str]
    ) -> bool:
        """
        Check if user has any of the specified permissions.

        Args:
            db: Database session
            user: User object
            permission_names: List of permission names to check

        Returns:
            True if user has any permission, False otherwise
        """
        for permission_name in permission_names:
            if await RBACService.user_has_permission(db, user, permission_name):
                return True
        return False

    @staticmethod
    async def user_has_all_permissions(
        db: AsyncSession,
        user: User,
        permission_names: List[str]
    ) -> bool:
        """
        Check if user has all of the specified permissions.

        Args:
            db: Database session
            user: User object
            permission_names: List of permission names to check

        Returns:
            True if user has all permissions, False otherwise
        """
        for permission_name in permission_names:
            if not await RBACService.user_has_permission(db, user, permission_name):
                return False
        return True

    @staticmethod
    async def get_user_permissions(
        db: AsyncSession,
        user: User
    ) -> List[str]:
        """
        Get all permission names for a user.

        Args:
            db: Database session
            user: User object

        Returns:
            List of permission names
        """
        permissions = set()

        for role in user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)

        return list(permissions)

    @staticmethod
    async def user_has_role(
        db: AsyncSession,
        user: User,
        role_name: str
    ) -> bool:
        """
        Check if user has a specific role.

        Args:
            db: Database session
            user: User object
            role_name: Role name to check

        Returns:
            True if user has role, False otherwise
        """
        for role in user.roles:
            if role.name == role_name:
                return True
        return False
