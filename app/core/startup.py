from sqlalchemy.ext.asyncio import AsyncEngine
from app.database import engine, Base
from fastapi import FastAPI

async def initalize_database(engine: AsyncEngine):
    """
    Runs tasks to initialize the database (e.g., create tables if not exist).
    """
    async with engine.begin() as conn:
        await conn.run_sync(lambda connection: Base.metadata.create_all(connection))
        
def register_startup(app: FastAPI):
    """
    Registers the on_startup event to initialize the database.
    """
    @app.on_event("startup")
    async def on_startup():
        # Initialize the database
        await initalize_database(engine)
        
def register_shutdown(app: FastAPI):
    """
    Registers the on_shutdown event to close the database connection.
    """
    @app.on_event("shutdown")
    async def on_shutdown():
       print("Shutting down")