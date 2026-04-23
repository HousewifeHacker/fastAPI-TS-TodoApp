import pytest_asyncio
import pytest
from sqlalchemy import text
from models import User, Todo
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import Base
import os

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/tododb"

@pytest_asyncio.fixture()
async def async_session():
    # Create a new engine and sessionmaker for each test
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    TestingSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with TestingSessionLocal() as session:
        yield session
    await engine.dispose()
    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_database_connection(async_session):
    result = await async_session.execute(text("SELECT 1"))
    val = result.scalar()
    assert val == 1

@pytest.mark.asyncio
async def test_create_user(async_session):
    user = User(username="testuser", password="pw123456")
    async_session.add(user)
    await async_session.commit()
    assert user.id is not None

@pytest.mark.asyncio
async def test_create_todo(async_session):
    user = User(username="testuser2", password="pw123456")
    async_session.add(user)
    await async_session.commit()
    todo = Todo(title="Test Todo", owner_id=user.id)
    async_session.add(todo)
    await async_session.commit()
    assert todo.id is not None
    assert todo.owner_id == user.id
    assert todo.completed == False

@pytest.mark.asyncio
async def test_update_todo(async_session):
    user = User(username="testuser3", password="pw123456")
    async_session.add(user)
    await async_session.commit()
    todo = Todo(title="Test Todo 2", owner_id=user.id)
    async_session.add(todo)
    await async_session.commit()
    todo.completed = True
    await async_session.commit()
    assert todo.completed == True

@pytest.mark.asyncio
async def test_delete_todo(async_session):
    user = User(username="testuser4", password="pw123456")
    async_session.add(user)
    await async_session.commit()
    todo = Todo(title="Test Todo 3", owner_id=user.id)
    async_session.add(todo)
    await async_session.commit()
    await async_session.delete(todo)
    await async_session.commit()
    result = await async_session.get(Todo, todo.id)
    assert result is None

@pytest.mark.asyncio
async def test_user_todo_list_relationship(async_session):
    user = User(username="testuser5", password="pw123456")
    async_session.add(user)
    await async_session.commit()
    todo1 = Todo(title="Test Todo 4", owner_id=user.id)
    todo2 = Todo(title="Test Todo 5", owner_id=user.id)
    async_session.add_all([todo1, todo2])
    await async_session.commit()
    todos = await async_session.execute(text("SELECT title FROM todos WHERE owner_id=:owner_id ORDER BY id"), {"owner_id": user.id})
    titles = [row[0] for row in todos.fetchall()]
    assert titles == ["Test Todo 4", "Test Todo 5"]

@pytest.mark.asyncio
async def test_user_unique_username(async_session):
    user1 = User(username="uniqueuser", password="pw123456")
    user2 = User(username="uniqueuser", password="pw123456")
    async_session.add(user1)
    await async_session.commit()
    async_session.add(user2)
    with pytest.raises(Exception):
        await async_session.commit()
        assert False, "Expected an exception due to unique constraint violation"
    assert True  # If we reach here, the exception was raised as expected