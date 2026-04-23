import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

#load_dotenv(dotenv_path="./backend/.env.backend")

#DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/tododb"
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
