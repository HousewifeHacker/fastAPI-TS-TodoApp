import os
from dotenv import load_dotenv

# 3rd party
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Docker: app runs from /app, .env.backend is in the same directory
# Local: app runs from backend/, need to go up one level
env_path = ".env.backend" if os.path.exists(".env.backend") else "../.env.backend"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
