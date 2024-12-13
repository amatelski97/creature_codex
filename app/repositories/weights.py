from psycopg_pool import AsyncConnectionPool
from typing import List, Optional
from datetime import date, datetime
from fastapi import HTTPException
from psycopg.rows import dict_row

async def add_weight(db_pool: AsyncConnectionPool, weight_data: dict) -> dict:
    async with db_pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory
        async with conn.cursor() as cur:
            query = """
                INSERT INTO weights (animal_id, weight, record_date)
                VALUES (%s, %s, %s)
                RETURNING id, animal_id, weight, record_date
            """
            await cur.execute(query, (weight_data["animal_id"], weight_data["weight"], weight_data["record_date"]))
            results = await cur.fetchone()
            await conn.commit()
            return results
        
async def get_weight_by_animal_id(db_pool: AsyncConnectionPool, weight_id: int) -> dict:
    async with db_pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory
        async with conn.cursor() as cur:
            query = "SELECT * FROM weights WHERE id = %s"
            await cur.execute(query, (weight_id,))
            results = await cur.fetchone()
            if results is None:
                raise HTTPException(status_code=404, detail=f"Weight with ID {weight_id} not found.")
            return results


async def get_all_weights(db_pool: AsyncConnectionPool) -> List[dict]:
    """
    Fetch all weights, returning them as a list of dictionaries.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, animal_id, weight, record_date FROM weights ORDER BY record_date DESC")
            results = await cur.fetchall()
            return results  # Already a list of dicts
