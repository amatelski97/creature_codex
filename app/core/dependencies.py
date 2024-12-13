from psycopg_pool import AsyncConnectionPool
from fastapi import Depends
from app.database import db_pool
from typing import AsyncGenerator

async def get_db() -> AsyncConnectionPool:
    """
    Dependency to provide access to the database pool.
    """
    return db_pool

async def get_db_connection() -> AsyncGenerator:
    """
    Dependency to provide a single database connection for a request.
    Ensures cleanup after the connection is used.
    """
    async with db_pool.connection() as connection:
        yield connection
