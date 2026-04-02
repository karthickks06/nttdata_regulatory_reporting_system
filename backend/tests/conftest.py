"""
Pytest Configuration and Fixtures
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.base import Base
from app.models import *  # Import all models


# Test database URL
TEST_DATABASE_URL = f"postgresql+asyncpg://test_user:test_pass@localhost:5432/test_regulatory_reporting"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session"""
    SessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with SessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def mock_chromadb(monkeypatch):
    """Mock ChromaDB client for testing"""
    class MockCollection:
        def __init__(self, name):
            self.name = name
            self.data = []

        def add(self, documents, metadatas, ids):
            for i, doc in enumerate(documents):
                self.data.append({
                    "id": ids[i],
                    "document": doc,
                    "metadata": metadatas[i] if metadatas else {}
                })

        def query(self, query_texts, n_results=10, where=None):
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]]
            }

        def delete(self, ids):
            self.data = [d for d in self.data if d["id"] not in ids]

    class MockChromaClient:
        def __init__(self):
            self.collections = {}

        def get_or_create_collection(self, name):
            if name not in self.collections:
                self.collections[name] = MockCollection(name)
            return self.collections[name]

    return MockChromaClient()


@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user"""
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def test_admin(db_session: AsyncSession):
    """Create a test admin user"""
    from app.models.user import User
    from app.core.security import get_password_hash

    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        full_name="Admin User",
        is_active=True,
        is_superuser=True
    )

    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)

    return admin


@pytest.fixture
def test_token(test_user):
    """Generate JWT token for test user"""
    from app.core.security import create_access_token

    return create_access_token(subject=str(test_user.id))


@pytest.fixture
def admin_token(test_admin):
    """Generate JWT token for admin user"""
    from app.core.security import create_access_token

    return create_access_token(subject=str(test_admin.id))
