from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
import pytest

from app.database import Base, get_db
from app.main import app

#TODO use test db
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/tododb"


@pytest_asyncio.fixture
async def engine():
    """Create a new engine for each test function."""
    engine = create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# Provide a new database session for each test
@pytest_asyncio.fixture
async def async_session(engine):
    async with engine.connect() as connection:
        session = AsyncSession(
            bind=connection, 
            expire_on_commit=False, 
        )

        yield session
        
        await session.close()


@pytest_asyncio.fixture
async def client(async_session):
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    from httpx import AsyncClient

    async with AsyncClient() as ac:
        yield ac

    app.dependency_overrides.clear()
