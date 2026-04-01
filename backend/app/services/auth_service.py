"""Authentication service"""

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.user import User
from app.models.session import Session
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
import uuid


class AuthService:
    """Service for authentication operations"""

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        username: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user by username and password.

        Args:
            db: Database session
            username: Username
            password: Password

        Returns:
            User object if authentication successful, None otherwise
        """
        result = await db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        # Update last login
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(last_login=datetime.utcnow())
        )
        await db.commit()

        return user

    @staticmethod
    async def create_session(
        db: AsyncSession,
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> tuple[str, Session]:
        """
        Create a new user session.

        Args:
            db: Database session
            user: User object
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Tuple of (access_token, session_object)
        """
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )

        # Create session record
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRY_DAYS)

        new_session = Session(
            session_id=session_id,
            user_id=user.id,
            token=access_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )

        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)

        return access_token, new_session

    @staticmethod
    async def revoke_session(
        db: AsyncSession,
        session_id: str
    ) -> bool:
        """
        Revoke a user session.

        Args:
            db: Database session
            session_id: Session ID to revoke

        Returns:
            True if session was revoked, False otherwise
        """
        result = await db.execute(
            select(Session).where(Session.session_id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            return False

        await db.delete(session)
        await db.commit()

        return True
