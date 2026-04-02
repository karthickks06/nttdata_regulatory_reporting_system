"""User management endpoints (Admin only)"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_user, get_current_superuser
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash
from app.core.logging import audit_logger

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Create a new user (Admin only).

    **IMPORTANT**: Only administrators can create users.
    There is no public registration endpoint.

    **Permissions**: Requires superuser access.
    """
    # Check if username exists
    existing_user = await db.scalar(
        select(User).where(User.username == user_data.username)
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Check if email exists
    existing_email = await db.scalar(
        select(User).where(User.email == user_data.email)
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Create user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        is_active=user_data.is_active if hasattr(user_data, 'is_active') else True,
        is_superuser=user_data.is_superuser if hasattr(user_data, 'is_superuser') else False
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Audit log
    audit_logger.info(
        f"User created | user_id={new_user.id} | username={new_user.username} | created_by={current_user.username}"
    )

    return new_user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search by username or email"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    List all users (Admin only).

    **Permissions**: Requires superuser access.

    **Filtering**:
    - `is_active`: Filter by active/inactive users
    - `search`: Search by username or email
    """
    query = select(User).options(
        selectinload(User.roles)
    )

    # Apply filters
    if is_active is not None:
        query = query.where(User.is_active == is_active)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.username.ilike(search_pattern)) |
            (User.email.ilike(search_pattern)) |
            (User.full_name.ilike(search_pattern))
        )

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    users = result.scalars().all()

    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get user by ID (Admin only).

    **Permissions**: Requires superuser access.
    """
    query = select(User).where(User.id == user_id).options(
        selectinload(User.roles)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Update user (Admin only).

    **Permissions**: Requires superuser access.

    **Note**: Password updates are optional. If not provided, password remains unchanged.
    """
    # Get user
    query = select(User).where(User.id == user_id).options(
        selectinload(User.roles)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)

    # Handle password separately
    if 'password' in update_data and update_data['password']:
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
    elif 'password' in update_data:
        update_data.pop('password')

    # Check username uniqueness if changed
    if 'username' in update_data and update_data['username'] != user.username:
        existing = await db.scalar(
            select(User).where(User.username == update_data['username'])
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )

    # Check email uniqueness if changed
    if 'email' in update_data and update_data['email'] != user.email:
        existing = await db.scalar(
            select(User).where(User.email == update_data['email'])
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

    # Apply updates
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    # Audit log
    audit_logger.info(
        f"User updated | user_id={user_id} | username={user.username} | updated_by={current_user.username}"
    )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Delete user (Admin only).

    **Permissions**: Requires superuser access.

    **Warning**: This is a hard delete. Consider deactivating users instead.
    """
    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    # Get user
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Audit log before deletion
    audit_logger.warning(
        f"User deleted | user_id={user_id} | username={user.username} | deleted_by={current_user.username}"
    )

    await db.delete(user)
    await db.commit()

    return None


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Deactivate user (Admin only).

    **Permissions**: Requires superuser access.

    **Recommended**: Use this instead of deleting users to maintain audit trails.
    """
    # Prevent self-deactivation
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = False
    await db.commit()
    await db.refresh(user)

    # Audit log
    audit_logger.info(
        f"User deactivated | user_id={user_id} | username={user.username} | deactivated_by={current_user.username}"
    )

    return user


@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Activate user (Admin only).

    **Permissions**: Requires superuser access.
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = True
    await db.commit()
    await db.refresh(user)

    # Audit log
    audit_logger.info(
        f"User activated | user_id={user_id} | username={user.username} | activated_by={current_user.username}"
    )

    return user


@router.post("/{user_id}/roles/{role_id}", response_model=UserResponse)
async def assign_role_to_user(
    user_id: UUID,
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Assign role to user (Admin only).

    **Permissions**: Requires superuser access.
    """
    # Get user with roles
    user_result = await db.execute(
        select(User).where(User.id == user_id).options(
            selectinload(User.roles)
        )
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get role
    role_result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = role_result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    # Check if already assigned
    if role in user.roles:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already assigned to user"
        )

    # Assign role
    user.roles.append(role)
    await db.commit()
    await db.refresh(user)

    # Audit log
    audit_logger.info(
        f"Role assigned | user_id={user_id} | role_id={role_id} | role_name={role.name} | assigned_by={current_user.username}"
    )

    return user


@router.delete("/{user_id}/roles/{role_id}", response_model=UserResponse)
async def remove_role_from_user(
    user_id: UUID,
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Remove role from user (Admin only).

    **Permissions**: Requires superuser access.
    """
    # Get user with roles
    user_result = await db.execute(
        select(User).where(User.id == user_id).options(
            selectinload(User.roles)
        )
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Find and remove role
    role_to_remove = None
    for role in user.roles:
        if role.id == role_id:
            role_to_remove = role
            break

    if not role_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not assigned to user"
        )

    user.roles.remove(role_to_remove)
    await db.commit()
    await db.refresh(user)

    # Audit log
    audit_logger.info(
        f"Role removed | user_id={user_id} | role_id={role_id} | role_name={role_to_remove.name} | removed_by={current_user.username}"
    )

    return user


@router.get("/stats/summary")
async def get_user_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get user statistics (Admin only).

    **Permissions**: Requires superuser access.
    """
    total_users = await db.scalar(select(func.count(User.id)))
    active_users = await db.scalar(
        select(func.count(User.id)).where(User.is_active == True)
    )
    superusers = await db.scalar(
        select(func.count(User.id)).where(User.is_superuser == True)
    )

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "superusers": superusers,
    }
