from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_database
from app.schemas.animal_profiles import AnimalProfileCreate, AnimalProfileResponse
from app.services.animal_profiles import (
    fetch_all_profiles,
    fetch_profile_by_id,
    add_new_profile,
    remove_profile,
    update_profile_by_id
)

router = APIRouter()

@router.get("", response_model=list[AnimalProfileResponse])
async def get_all_profiles(db: AsyncSession = Depends(get_database)):
    """
    route to fetch all animal profiles
    """
    return await fetch_all_profiles(db)

@router.get("/{profile_id}", response_model=AnimalProfileResponse)
async def get_profile_by_id(profile_id: int, db: AsyncSession = Depends(get_database)):
    """
    route to fetch an animal profile by its ID
    """
    return await fetch_profile_by_id(db, profile_id)

@router.post("", response_model=AnimalProfileResponse)
async def create_profile(
    profile_data: AnimalProfileCreate,
    db: AsyncSession = Depends(get_database)  # Dependency injection for AsyncSession
):
    return await add_new_profile(db, profile_data.dict())

@router.put("/{profile_id}", response_model=AnimalProfileResponse)
async def update_profile(
    profile_id: int,
    profile_data: AnimalProfileCreate,
    db: AsyncSession = Depends(get_database),
):
    try:
        updated_profile = await update_profile_by_id(db, profile_id, profile_data.dict())
        return updated_profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("{profile_id}")
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_database)):
    """
    route to delete an animal profile by its ID
    """
    try:
        return await remove_profile(db, profile_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))