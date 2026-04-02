"""PostgreSQL database connection and session management"""

import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create async engine with connection pooling
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={
        "server_settings": {"application_name": "nttdata_regulatory_reporting"},
        "command_timeout": 60,
    },
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database sessions.

    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database - create all tables.

    This should be called on application startup.
    """
    try:
        async with engine.begin() as conn:
            # Import all models to register them with Base.metadata
            from app.db.base import Base

            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def check_db_connection() -> bool:
    """
    Check if database connection is healthy.

    Returns:
        bool: True if connection is healthy, False otherwise
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


async def close_db() -> None:
    """
    Close database connections.

    This should be called on application shutdown.
    """
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")
        raise


async def get_db_info() -> dict:
    """
    Get database information and statistics.

    Returns:
        dict: Database information
    """
    try:
        async with engine.connect() as conn:
            # Get PostgreSQL version
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()

            # Get database size
            result = await conn.execute(text(
                "SELECT pg_database_size(current_database())"
            ))
            size = result.scalar()

            # Get connection count
            result = await conn.execute(text(
                "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()"
            ))
            connections = result.scalar()

            return {
                "version": version,
                "size_bytes": size,
                "active_connections": connections,
                "pool_size": engine.pool.size(),
                "checked_in_connections": engine.pool.checkedin(),
            }
    except Exception as e:
        logger.error(f"Error getting database info: {e}")
        return {"error": str(e)}


# Session context manager for use outside of FastAPI dependencies
class DatabaseSession:
    """Context manager for database sessions."""

    def __init__(self):
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
            await self.session.close()
