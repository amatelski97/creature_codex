from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Database connection URL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1597@localhost:5432/creature_codex_live"

# Create the async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create sessionmaker for async sessions
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get the async database session
async def get_db():
    async with SessionLocal() as db:
        yield db