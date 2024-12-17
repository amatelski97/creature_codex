import os
from psycopg import connect
from app.core.config import settings
from app.utils.logger import setup_logger
import logging
from app.database import db_pool
 
logger = setup_logger()

async def on_startup():
    logger.info("Starting application...")
    if db_pool:
        logger.info(f"Database pool initialized: {db_pool}")
    else:
        logger.error("Database pool failed to initialize.")

def run_migrations():
    """
    Execute all SQL migration files in order from the migrations folder.
    Applies only migrations not yet recorded in the version control table.
    """
    migration_folder = "migrations/"
    with connect(settings.DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # Ensure the version control table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS migration_versions (
                    id SERIAL PRIMARY KEY,
                    filename TEXT NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logger.info("Version control table ensured.")

            # Apply migrations not already applied
            for file in sorted(os.listdir(migration_folder)):
                if file.endswith(".sql"):
                    cur.execute("SELECT filename FROM migration_versions WHERE filename = %s", (file,))
                    if cur.fetchone() is None:  # If migration not applied yet
                        with open(os.path.join(migration_folder, file), "r") as sql_file:
                            try:
                                cur.execute(sql_file.read())
                                cur.execute("INSERT INTO migration_versions (filename) VALUES (%s)", (file,))
                                conn.commit()
                                logger.info(f"Applied migration: {file}")
                            except Exception as e:
                                logger.error(f"Failed to apply migration {file}: {e}")
                                conn.rollback()  # Rollback on error

def register_startup(app):
    @app.on_event("startup")
    async def on_startup():
        run_migrations()
        logger.info("Startup logic complete")

def register_shutdown(app):
    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Shutdown logic complete")

