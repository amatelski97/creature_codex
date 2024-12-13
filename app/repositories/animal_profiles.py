from psycopg_pool import AsyncConnectionPool
from typing import List, Optional
import psycopg
import logging
from app.database import db_pool

async def get_all_profiles(conn, category: str | None = None) -> List[dict]:
    async with conn.cursor() as cur:
        if category:
            query = """
                SELECT id, name, species, scientific_name, age, gender, category,
                       TO_CHAR(latest_record_date, 'YYYY-MM-DD') AS latest_record_date
                FROM animal_profiles
                WHERE category = %s
            """
            await cur.execute(query, (category,))
        else:
            query = """
                SELECT id, name, species, scientific_name, age, gender, category,
                       TO_CHAR(latest_record_date, 'YYYY-MM-DD') AS latest_record_date
                FROM animal_profiles
            """
            await cur.execute(query)

        rows = await cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        return [dict(zip(col_names, row)) for row in rows]

async def get_profile_by_id(db_pool: AsyncConnectionPool, profile_id: int) -> Optional[dict]:
    """
    Retrieve a single animal profile by its ID.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(cursor_factory=psycopg.rows.dict_row) as cur:
            await cur.execute("SELECT * FROM animal_profiles WHERE id = %s", (profile_id,))
            row = await cur.fetchone()
            return dict(row) if row else None

async def create_profile(db_pool: AsyncConnectionPool, profile_data: dict) -> dict:
    """
    Insert a new animal profile into the database.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(cursor_factory=psycopg.rows.dict_row) as cur:
            query = """
                INSERT INTO animal_profiles (name, species, scientific_name, age, gender, category)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
            """
            await cur.execute(
                query,
                (
                    profile_data["name"],
                    profile_data["species"],
                    profile_data.get("scientific_name"),
                    profile_data.get("age"),
                    profile_data["gender"],
                    profile_data["category"],
                )
            )
            row = await cur.fetchone()
            await conn.commit()
            return dict(row)

async def delete_profile(db_pool: AsyncConnectionPool, profile_id: int) -> bool:
    """
    Delete an animal profile by ID.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM animal_profiles WHERE id = %s", (profile_id,))
            if cur.rowcount == 0:
                raise ValueError(f"Profile with ID {profile_id} not found.")
            await conn.commit()
            return True

async def update_profile(db_pool: AsyncConnectionPool, profile_id: int, profile_data: dict) -> dict:
    """
    Update an existing animal profile by ID.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            # Dynamically generate the update query
            fields = ", ".join(f"{key} = %s" for key in profile_data.keys())
            query = f"""
                UPDATE animal_profiles
                SET {fields}
                WHERE id = %s
                RETURNING *
            """
            params = list(profile_data.values()) + [profile_id]
            await cur.execute(query, params)
            row = await cur.fetchone()
            if not row:
                raise ValueError(f"Profile with ID {profile_id} not found.")
            await conn.commit()
            return dict(row)