from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.animal_profiles import (
    get_all_profiles,
    get_profile_by_id,
    create_profile,
    delete_profile,
)

async def fetch_all_profiles(db: AsyncSession):
    """
    Fetch all animal profiles from the database.
    """
    return await get_all_profiles(db)

async def fetch_profile_by_id(db: AsyncSession, profile_id: int):
    """
    Fetch an animal profile by its ID.
    """
    profile= await get_profile_by_id(db, profile_id)
    if not profile: 
        raise ValueError(f"profile with ID {profile_id} not found.")
    return profile

async def add_new_profile(db: AsyncSession, profile_data: dict):
    """
    Add a new animal profile to the database.
    """
    return await create_profile(db, profile_data)

async def update_profile_by_id(db: AsyncSession, profile_id: int, profile_data: dict):
    """
    Update an existing animal profile by its ID
    """
    # Fetch the existing profile
    profile = await fetch_profile_by_id(db, profile_id)
    if not profile:
        raise ValueError("Profile not found.")

    # Update the fields
    for key, value in profile_data.items():
        setattr(profile, key, value)

    # Commit and refresh
    await db.commit()
    await db.refresh(profile)
    return profile
async def remove_profile(db: AsyncSession, profile_id: int):
    """
    Remove an animal profile from the database.
    """
    success = await delete_profile(db, profile_id)
    if not success:
        raise ValueError(f"Profile with ID {profile_id} not found or could not be deleted.")
    return {"message": f"Profile with ID {profile_id} has been deleted."}