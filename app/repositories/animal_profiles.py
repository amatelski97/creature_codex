from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models import AnimalProfiles

async def get_all_profiles(db: AsyncSession):
    """
    Get all animal profiles from the database.
    """
    result = await db.execute(select(AnimalProfiles))
    return result.scalars().all()

async def get_profile_by_id(db: AsyncSession, profile_id: int):
    """
    Get an animal profile by its ID.
    """
    result = await db.execute(select(AnimalProfiles).where(AnimalProfiles.id == profile_id))
    return result.scalar_one_or_none()

async def create_profile(db: AsyncSession, profile_data: dict):
    """
    Create a new animal profile in the database.
    """
    new_profile = AnimalProfiles(**profile_data)
    db.add(new_profile)
    try:
        await db.commit()
        await db.refresh(new_profile)
        return new_profile
    except IntegrityError:
        await db.rollback()
        raise ValueError("could not creat the animal profile (possible duplicate).")

async def delete_profile(db: AsyncSession, profile_id: int):
    """
    Delete an animal profile by ID
    """
    profile = await get_profile_by_id(db, profile_id)
    if not profile:
        raise ValueError(f"Profile with ID {profile_id} not found.")    
    await db.delete(profile)
    await db.commit()
    return True

