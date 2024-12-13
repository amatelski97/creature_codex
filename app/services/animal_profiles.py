from psycopg.rows import class_row
from app.repositories.animal_profiles import (
    get_all_profiles,
    get_profile_by_id,
    create_profile,
    delete_profile,
)
from app.models import AnimalProfiles

async def fetch_all_profiles(db_pool):
    """
    Fetch all animal profiles from the database.
    """
    async with db_pool.connection() as conn:
        return await get_all_profiles(conn)

async def fetch_profile_by_id(db_pool, profile_id: int):
    """
    Fetch an animal profile by its ID.
    """
    async with db_pool.connection() as conn:
        profile = await get_profile_by_id(conn, profile_id)
        if not profile:
            raise ValueError(f"Profile with ID {profile_id} not found.")
        return profile

async def fetch_profiles(db_pool, category: str | None = None):
    """
    Fetch animal profiles filtered by category (if provided).
    """
    async with db_pool.connection() as conn:
        if category:
            query = "SELECT * FROM animal_profiles WHERE category = %s"
            result = await conn.execute(query, (category,))
        else:
            query = "SELECT * FROM animal_profiles"
            result = await conn.execute(query)
        return [AnimalProfiles(**row) for row in result]

async def add_new_profile(db_pool, profile_data: dict):
    """
    Add a new animal profile to the database.
    """
    async with db_pool.connection() as conn:
        return await create_profile(conn, profile_data)

async def update_profile_by_id(db_pool, profile_id: int, profile_data: dict):
    """
    Update an existing animal profile by its ID.
    """
    async with db_pool.connection() as conn:
        profile = await get_profile_by_id(conn, profile_id)
        if not profile:
            raise ValueError(f"Profile with ID {profile_id} not found.")

        # Update the fields
        update_query = """
        UPDATE animal_profiles
        SET name = %s, species = %s, scientific_name = %s, age = %s, gender = %s, category = %s
        WHERE id = %s
        RETURNING *;
        """
        updated_profile = await conn.execute(
            update_query,
            (
                profile_data.get("name", profile.name),
                profile_data.get("species", profile.species),
                profile_data.get("scientific_name", profile.scientific_name),
                profile_data.get("age", profile.age),
                profile_data.get("gender", profile.gender),
                profile_data.get("category", profile.category),
                profile_id,
            ),
        )
        return updated_profile

async def remove_profile(db_pool, profile_id: int):
    """
    Remove an animal profile from the database.
    """
    async with db_pool.connection() as conn:
        success = await delete_profile(conn, profile_id)
        if not success:
            raise ValueError(f"Profile with ID {profile_id} not found or could not be deleted.")
        return {"message": f"Profile with ID {profile_id} has been deleted."}
