from psycopg_pool import AsyncConnectionPool
from psycopg import sql
from typing import List
from datetime import date
from fastapi import HTTPException
from psycopg.rows import dict_row

async def add_deep_clean(db_pool: AsyncConnectionPool, clean_data: dict) -> dict:
    """
    Add a new deep clean entry.
    """
    async with db_pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory
        async with conn.cursor() as cur:
            query = """
                INSERT INTO deep_cleans (animal_id, clean_date, cleaner_name, notes)
                VALUES (%s, %s, %s, %s)
                RETURNING id, animal_id, clean_date, cleaner_name, notes
            """
            await cur.execute(query, (clean_data["animal_id"], clean_data["clean_date"], clean_data["cleaner_name"], clean_data["notes"]))
            new_clean = await cur.fetchone()
            await conn.commit()
            return new_clean

async def get_deep_clean_by_id(db_pool: AsyncConnectionPool, clean_id: int) -> dict:
    """
    Retrieve a specific deep clean entry by its ID.
    """
    async with db_pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory
        async with conn.cursor() as cur:
            query = "SELECT * FROM deep_cleans WHERE id = %s"
            await cur.execute(query, (clean_id,))
            clean = await cur.fetchone()
            if clean is None:
                raise HTTPException(status_code=404, detail=f"Deep clean entry with ID {clean_id} not found.")
            return clean

async def get_all_deep_cleans(db_pool: AsyncConnectionPool) -> List[dict]:
    """
    Retrieve all deep clean entries.
    """
    async with db_pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM deep_cleans ORDER BY clean_date DESC")
            results = await cur.fetchall()
            return results

async def update_deep_clean(db_pool: AsyncConnectionPool, clean_id: int, clean_data: dict) -> dict:
    """
    Update an existing deep clean entry by its ID.
    """
    async with db_pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory
        async with conn.cursor() as cur:
            # Ensure the deep clean entry exists
            query_select = "SELECT * FROM deep_cleans WHERE id = %s"
            await cur.execute(query_select, (clean_id,))
            existing_clean = await cur.fetchone()
            if not existing_clean:
                raise HTTPException(status_code=404, detail=f"Deep clean entry with ID {clean_id} not found.")

            # Perform the update
            query_update = """
                UPDATE deep_cleans
                SET clean_date = %s, cleaner_name = %s, notes = %s
                WHERE id = %s
                RETURNING id, animal_id, clean_date, cleaner_name, notes
            """
            await cur.execute(query_update, (clean_data["clean_date"], clean_data["cleaner_name"], clean_data["notes"], clean_id))
            updated_clean = await cur.fetchone()
            await conn.commit()
            return updated_clean

async def delete_deep_clean(db_pool: AsyncConnectionPool, clean_id: int) -> bool:
    """
    Delete a deep clean entry by its ID.
    """
    async with db_pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory
        async with conn.cursor() as cur:
            # Ensure the deep clean entry exists
            query_select = "SELECT id FROM deep_cleans WHERE id = %s"
            await cur.execute(query_select, (clean_id,))
            existing_clean = await cur.fetchone()
            if not existing_clean:
                raise HTTPException(status_code=404, detail=f"Deep clean entry with ID {clean_id} not found.")

            # Perform the deletion
            query_delete = "DELETE FROM deep_cleans WHERE id = %s"
            await cur.execute(query_delete, (clean_id,))
            await conn.commit()
            return True
