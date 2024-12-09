from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Define the declarative base
Base = declarative_base()

# Create an async database engine
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
)

# Create an async session maker
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to provide database sessions
from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    Ensures proper cleanup after use.
    """
    async with async_session_maker() as session:
        yield session