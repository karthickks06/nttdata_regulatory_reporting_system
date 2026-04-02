"""Role-Based Access Control (RBAC) implementation"""

import logging
from typing import List, Optional, Set, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

logger = logging.getLogger(__name__)


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

        # Check if user is active
        if not user.is_active:
            return False

        # Check user's roles for the permission
        for role in user.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True

        return False

    @staticmethod
    async def user_has_resource_permission(
        db: AsyncSession,
        user: User,
        resource: str,
        action: str
    ) -> bool:
        """
        Check if user has permission for a specific resource and action.

        Args:
            db: Database session
            user: User object
            resource: Resource type (e.g., 'reports', 'users')
            action: Action type (e.g., 'read', 'write', 'delete')

        Returns:
            True if user has permission, False otherwise
        """
        permission_name = f"{resource}.{action}"
        return await RBACService.user_has_permission(db, user, permission_name)

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
        if user.is_superuser:
            return True

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
        if user.is_superuser:
            return True

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
        permissions: Set[str] = set()

        # Load user with roles and permissions
        stmt = select(User).where(User.id == user.id).options(
            selectinload(User.roles).selectinload(Role.permissions)
        )
        result = await db.execute(stmt)
        user_with_perms = result.scalar_one_or_none()

        if user_with_perms:
            for role in user_with_perms.roles:
                for permission in role.permissions:
                    permissions.add(permission.name)

        return sorted(list(permissions))

    @staticmethod
    async def get_user_roles(
        db: AsyncSession,
        user: User
    ) -> List[str]:
        """
        Get all role names for a user.

        Args:
            db: Database session
            user: User object

        Returns:
            List of role names
        """
        return [role.name for role in user.roles]

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

    @staticmethod
    async def user_has_any_role(
        db: AsyncSession,
        user: User,
        role_names: List[str]
    ) -> bool:
        """
        Check if user has any of the specified roles.

        Args:
            db: Database session
            user: User object
            role_names: List of role names to check

        Returns:
            True if user has any role, False otherwise
        """
        user_role_names = {role.name for role in user.roles}
        return bool(user_role_names.intersection(set(role_names)))

    @staticmethod
    async def assign_role_to_user(
        db: AsyncSession,
        user: User,
        role_id: UUID
    ) -> bool:
        """
        Assign a role to a user.

        Args:
            db: Database session
            user: User object
            role_id: Role ID to assign

        Returns:
            True if successful, False otherwise
        """
        try:
            stmt = select(Role).where(Role.id == role_id)
            result = await db.execute(stmt)
            role = result.scalar_one_or_none()

            if not role:
                logger.warning(f"Role {role_id} not found")
                return False

            # Check if user already has this role
            if role in user.roles:
                logger.info(f"User {user.id} already has role {role.name}")
                return True

            user.roles.append(role)
            await db.commit()
            logger.info(f"Assigned role {role.name} to user {user.id}")
            return True

        except Exception as e:
            logger.error(f"Error assigning role to user: {e}")
            await db.rollback()
            return False

    @staticmethod
    async def remove_role_from_user(
        db: AsyncSession,
        user: User,
        role_id: UUID
    ) -> bool:
        """
        Remove a role from a user.

        Args:
            db: Database session
            user: User object
            role_id: Role ID to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            # Find the role in user's roles
            role_to_remove = None
            for role in user.roles:
                if role.id == role_id:
                    role_to_remove = role
                    break

            if not role_to_remove:
                logger.warning(f"User {user.id} does not have role {role_id}")
                return False

            user.roles.remove(role_to_remove)
            await db.commit()
            logger.info(f"Removed role {role_to_remove.name} from user {user.id}")
            return True

        except Exception as e:
            logger.error(f"Error removing role from user: {e}")
            await db.rollback()
            return False

    @staticmethod
    async def get_users_with_permission(
        db: AsyncSession,
        permission_name: str
    ) -> List[User]:
        """
        Get all users with a specific permission.

        Args:
            db: Database session
            permission_name: Permission name

        Returns:
            List of users
        """
        stmt = (
            select(User)
            .join(User.roles)
            .join(Role.permissions)
            .where(Permission.name == permission_name)
            .options(selectinload(User.roles))
        )
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    @staticmethod
    async def get_users_with_role(
        db: AsyncSession,
        role_name: str
    ) -> List[User]:
        """
        Get all users with a specific role.

        Args:
            db: Database session
            role_name: Role name

        Returns:
            List of users
        """
        stmt = (
            select(User)
            .join(User.roles)
            .where(Role.name == role_name)
            .options(selectinload(User.roles))
        )
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    @staticmethod
    async def get_permission_matrix(
        db: AsyncSession,
        user: User
    ) -> Dict[str, List[str]]:
        """
        Get a matrix of permissions grouped by resource.

        Args:
            db: Database session
            user: User object

        Returns:
            Dictionary mapping resource names to lists of actions
        """
        permissions = await RBACService.get_user_permissions(db, user)
        matrix: Dict[str, List[str]] = {}

        for perm in permissions:
            if '.' in perm:
                resource, action = perm.split('.', 1)
                if resource not in matrix:
                    matrix[resource] = []
                matrix[resource].append(action)

        return matrix
