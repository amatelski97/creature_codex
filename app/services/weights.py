from psycopg import sql
from psycopg.rows import dict_row
from datetime import date

import logging

logger = logging.getLogger("uvicorn.error")

async def add_weight(db_pool, animal_id: int, weight: float, record_date: date):
    """
    Add a new weight entry and update the animal's latest weight and record date.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Insert the new weight record
            insert_query = sql.SQL("""
                INSERT INTO weights (animal_id, weight, record_date)
                VALUES (%s, %s, %s)
                RETURNING id, animal_id, weight, record_date
            """)
            await cur.execute(insert_query, (animal_id, weight, record_date))
            new_weight = await cur.fetchone()

            # Update the animal profile's latest weight and record date
            update_query = sql.SQL("""
                UPDATE animal_profiles
                SET latest_weight = %s, latest_record_date = %s
                WHERE id = %s
            """)
            await cur.execute(update_query, (weight, record_date, animal_id))
            await conn.commit()

            return new_weight  # Return the inserted weight as a dictionary

async def update_weight(db_pool, weight_id: int, new_weight: float, new_record_date: date):
    """
    Update an existing weight entry and refresh the animal profile's latest weight/date if needed.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Update the weight entry
            update_weight_query = sql.SQL("""
                UPDATE weights
                SET weight = %s, record_date = %s
                WHERE id = %s
                RETURNING animal_id
            """)
            await cur.execute(update_weight_query, (new_weight, new_record_date, weight_id))
            result = await cur.fetchone()

            if not result:
                raise ValueError(f"Weight with ID {weight_id} not found.")

            animal_id = result['animal_id']

            # Update the animal profile with the latest weight and date
            update_latest_query = sql.SQL("""
                UPDATE animal_profiles
                SET latest_weight = subquery.weight, latest_record_date = subquery.record_date
                FROM (
                    SELECT weight, record_date
                    FROM weights
                    WHERE animal_id = %s
                    ORDER BY record_date DESC
                    LIMIT 1
                ) AS subquery
                WHERE animal_profiles.id = %s
            """)
            await cur.execute(update_latest_query, (animal_id, animal_id))
            await conn.commit()

            return {"id": weight_id, "animal_id": animal_id, "weight": new_weight, "record_date": new_record_date}

async def delete_weight(db_pool, weight_id: int):
    """
    Delete a weight entry and ensure the latest weight for the animal is updated.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Fetch the animal ID associated with the weight
            get_animal_id_query = sql.SQL("""
                SELECT animal_id FROM weights WHERE id = %s
            """)
            await cur.execute(get_animal_id_query, (weight_id,))
            result = await cur.fetchone()

            if not result:
                raise ValueError(f"Weight with ID {weight_id} not found.")

            animal_id = result['animal_id']

            # Delete the weight record
            delete_query = sql.SQL("""
                DELETE FROM weights WHERE id = %s
            """)
            await cur.execute(delete_query, (weight_id,))

            # Update the animal profile's latest weight and date
            update_latest_query = sql.SQL("""
                UPDATE animal_profiles
                SET latest_weight = subquery.weight, latest_record_date = subquery.record_date
                FROM (
                    SELECT weight, record_date
                    FROM weights
                    WHERE animal_id = %s
                    ORDER BY record_date DESC
                    LIMIT 1
                ) AS subquery
                WHERE animal_profiles.id = %s
            """)
            await cur.execute(update_latest_query, (animal_id, animal_id))
            await conn.commit()

            return True  # Indicate successful deletion

async def get_weight_by_id(db_pool, weight_id: int) -> dict:
    """
    Retrieve a specific weight entry by its ID.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            query = sql.SQL("""
                SELECT * FROM weights WHERE id = %s
            """)
            await cur.execute(query, (weight_id,))
            result = await cur.fetchone()

            if not result:
                raise ValueError(f"Weight with ID {weight_id} not found.")

            return result  # Return the row as a dictionary

async def get_all_weights(db_pool, animal_id: int = None) -> list[dict]:
    """
    Retrieve all weight entries, optionally filtered by animal_id.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            if animal_id is not None:
                query = sql.SQL("""
                    SELECT * FROM weights WHERE animal_id = %s ORDER BY record_date DESC
                """)
                await cur.execute(query, (animal_id,))
            else:
                query = sql.SQL("""
                    SELECT * FROM weights ORDER BY record_date DESC
                """)
                await cur.execute(query)
            results = await cur.fetchall()
            return results  # Already a list of dicts
