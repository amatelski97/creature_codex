from psycopg import sql
from psycopg.rows import dict_row
from datetime import date
from fastapi import HTTPException

async def add_deep_clean(db_pool, clean_data: dict) -> dict:
    """
    Add a new deep clean entry.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Insert the new deep clean record
            insert_query = sql.SQL("""
                INSERT INTO deep_cleans (animal_id, clean_date, cleaner_name, notes)
                VALUES (%s, %s, %s, %s)
                RETURNING id, animal_id, clean_date, cleaner_name, notes
            """)
            await cur.execute(
                insert_query,
                (clean_data["animal_id"], clean_data["clean_date"], clean_data["cleaner_name"], clean_data["notes"]),
            )
            new_clean = await cur.fetchone()
            await conn.commit()
            return new_clean  # Return the newly created record

async def get_deep_clean_by_id(db_pool, clean_id: int) -> dict:
    """
    Retrieve a specific deep clean entry by its ID.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            query = sql.SQL("""
                SELECT * FROM deep_cleans WHERE id = %s
            """)
            await cur.execute(query, (clean_id,))
            clean = await cur.fetchone()

            if not clean:
                raise HTTPException(status_code=404, detail=f"Deep clean entry with ID {clean_id} not found.")

            return clean  # Return the row as a dictionary

async def get_all_deep_cleans(db_pool, animal_id: int = None) -> list[dict]:
    """
    Retrieve all deep clean entries, optionally filtered by animal_id.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            if animal_id is not None:
                query = sql.SQL("""
                    SELECT * FROM deep_cleans WHERE animal_id = %s ORDER BY clean_date DESC
                """)
                await cur.execute(query, (animal_id,))
            else:
                query = sql.SQL("""
                    SELECT * FROM deep_cleans ORDER BY clean_date DESC
                """)
                await cur.execute(query)
            results = await cur.fetchall()
            return results  # Return a list of rows as dictionaries

async def update_deep_clean(db_pool, clean_id: int, clean_data: dict) -> dict:
    """
    Update an existing deep clean entry by its ID.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Ensure the entry exists
            query_select = sql.SQL("""
                SELECT * FROM deep_cleans WHERE id = %s
            """)
            await cur.execute(query_select, (clean_id,))
            existing_clean = await cur.fetchone()

            if not existing_clean:
                raise HTTPException(status_code=404, detail=f"Deep clean entry with ID {clean_id} not found.")

            # Update the entry
            query_update = sql.SQL("""
                UPDATE deep_cleans
                SET clean_date = %s, cleaner_name = %s, notes = %s
                WHERE id = %s
                RETURNING id, animal_id, clean_date, cleaner_name, notes
            """)
            await cur.execute(
                query_update,
                (clean_data["clean_date"], clean_data["cleaner_name"], clean_data["notes"], clean_id),
            )
            updated_clean = await cur.fetchone()
            await conn.commit()
            return updated_clean  # Return the updated record

async def delete_deep_clean(db_pool, clean_id: int) -> bool:
    """
    Delete a deep clean entry by its ID.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Ensure the entry exists
            query_select = sql.SQL("""
                SELECT id FROM deep_cleans WHERE id = %s
            """)
            await cur.execute(query_select, (clean_id,))
            existing_clean = await cur.fetchone()

            if not existing_clean:
                raise HTTPException(status_code=404, detail=f"Deep clean entry with ID {clean_id} not found.")

            # Delete the record
            delete_query = sql.SQL("""
                DELETE FROM deep_cleans WHERE id = %s
            """)
            await cur.execute(delete_query, (clean_id,))
            await conn.commit()

            return True  # Indicate successful deletion
