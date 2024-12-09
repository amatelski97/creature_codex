from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import async_session_maker
from typing import AsyncGenerator

async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an asynchronous database session.
    Ensures proper cleanup after each request.
    """
    async with async_session_maker() as session:
        yield session
