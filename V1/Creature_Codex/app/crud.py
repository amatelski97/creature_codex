from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Profiles
from app.schemas import ProfilesCreate


async def create_profiles(db: AsyncSession, profile: ProfilesCreate):
    """
    Create a new profile in the database.
    """
    db_profile = Profiles(**profile.dict())
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile


async def get_profiles(db: AsyncSession):
    """
    Retrieve all profiles from the database.
    """
    result = await db.execute(select(Profiles))
    return result.scalars().all()


async def get_profile(db: AsyncSession, profile_id: int):
    """
    Retrieve a single profile by its ID.
    """
    result = await db.execute(select(Profiles).where(Profiles.id == profile_id))
    return result.scalar_one_or_none()


async def update_profile(db: AsyncSession, profile_id: int, profile: ProfilesCreate):
    """
    Update an existing profile by its ID.
    """
    result = await db.execute(select(Profiles).where(Profiles.id == profile_id))
    db_profile = result.scalar_one_or_none()
    if db_profile:
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)
        await db.commit()
        await db.refresh(db_profile)
    return db_profile


async def delete_profile(db: AsyncSession, profile_id: int):
    """
    Delete a profile by its ID.
    """
    result = await db.execute(select(Profiles).where(Profiles.id == profile_id))
    db_profile = result.scalar_one_or_none()
    if db_profile:
        await db.delete(db_profile)
        await db.commit()
    return db_profile


async def search_profiles(
    db: AsyncSession,
    name: str = None,
    species: str = None,
    scientific_name: str = None,
    gender: str = None,
):
    """
    Search profiles by optional filters.
    """
    query = select(Profiles)
    if name:
        query = query.where(Profiles.name.ilike(f"%{name}%"))
    if species:
        query = query.where(Profiles.species.ilike(f"%{species}%"))
    if scientific_name:
        query = query.where(Profiles.scientific_name.ilike(f"%{scientific_name}%"))
    if gender:
        query = query.where(Profiles.gender == gender)

    result = await db.execute(query)
    return result.scalars().all()


async def bulk_insert_profiles(db: AsyncSession, profiles: list[ProfilesCreate]):
    """
    Bulk insert multiple profiles from a CSV or other input source.
    """
    try:
        db_profiles = [Profiles(**profile.dict()) for profile in profiles]
        db.add_all(db_profiles)
        await db.commit()
        return db_profiles
    except Exception as e:
        await db.rollback()
        print(f"Error during bulk insert: {e}")
        raise

