from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from app.core.config import settings
from psycopg.rows import dict_row

# Define the connection pool for psycopg
db_pool = AsyncConnectionPool(
    conninfo=settings.DATABASE_URL,  # Connection string
    min_size=1,  # Minimum connections in the pool
    max_size=10,  # Maximum connections in the pool
    open=False
)
async def initialize_pool():
    """
    Open the connection pool.
    """
    await db_pool.open()

async def close_pool():
    """
    Close the connection pool.
    """
    await db_pool.close()

@asynccontextmanager
async def get_db_connection():
    """
    Dependency that provides a database connection.
    Ensures proper cleanup after use.
    """
    async with db_pool.connection() as conn:
        # Specify default cursor factory (if necessary)
        async with conn.cursor() as cursor:
            yield cursor

async def init_db():
    pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        min_size=1,
        max_size=5,
        kwargs={"autocommit": True, "row_factory": dict_row},  # Enable autocommit
        configure=lambda conn: conn.execute("SET TIME ZONE 'UTC'")
    )
    return pool