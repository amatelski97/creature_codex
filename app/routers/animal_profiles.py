from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from psycopg_pool import AsyncConnectionPool
from app.core.dependencies import get_db_connection
from app.schemas.animal_profiles import AnimalProfileCreate, AnimalProfileResponse
from app.repositories.animal_profiles import (
    get_all_profiles,
    get_profile_by_id,
    get_profile_by_category_and_id,  # Added
    create_profile,
    delete_profile,
    update_profile,
)

router = APIRouter()

@router.get("/all", response_model=list[AnimalProfileResponse])
async def fetch_all_profiles(db_pool: AsyncConnectionPool = Depends(get_db_connection)):
    """
    Fetch all animal profiles.
    """
    return await get_all_profiles(db_pool)

@router.get("/", response_model=list[AnimalProfileResponse])
async def fetch_profiles_by_category(
    category: str | None = Query(None, description="Filter by animal category"),
    db_pool: AsyncConnectionPool = Depends(get_db_connection),
):
    """
    Fetch animal profiles, optionally filtered by category.
    """
    return await get_all_profiles(db_pool, category)

@router.get("/{profile_id}", response_model=AnimalProfileResponse)
async def fetch_profile_by_id(profile_id: int, db_pool: AsyncConnectionPool = Depends(get_db_connection)):
    """
    Fetch a single animal profile by its ID.
    """
    profile = await get_profile_by_id(db_pool, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/", response_model=list[AnimalProfileResponse])
async def fetch_profiles_by_category(
    category: str = Query(..., description="Filter by animal category"),
    db_pool: AsyncConnectionPool = Depends(get_db_connection),
):
    """
    Fetch animal profiles filtered by category.
    """
    profiles = await get_all_profiles(db_pool, category)
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found")
    return profiles

@router.get("/{category}/{id}", response_model=AnimalProfileResponse)
async def fetch_profile_by_category_and_id(
    category: str,
    id: int,
    db_pool: AsyncConnectionPool = Depends(get_db_connection),
):
    """
    Fetch a single animal profile by category and ID.
    """
    profile = await get_profile_by_category_and_id(db_pool, id, category)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("", response_model=AnimalProfileResponse)
async def add_profile(
    profile_data: AnimalProfileCreate, 
    db_pool: AsyncConnectionPool = Depends(get_db_connection)
):
    """
    Add a new animal profile.
    """
    return await create_profile(db_pool, profile_data)

@router.put("/{profile_id}", response_model=AnimalProfileResponse)
async def modify_profile(
    profile_id: int,
    profile_data: AnimalProfileCreate,
    db_pool: AsyncConnectionPool = Depends(get_db_connection),
):
    """
    Update an animal profile by ID.
    """
    updated_profile = await update_profile(db_pool, profile_id, profile_data.model_dump())
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile

@router.delete("/{profile_id}")
async def remove_profile(profile_id: int, db_pool: AsyncConnectionPool = Depends(get_db_connection)):
    """
    Delete an animal profile by ID.
    """
    success = await delete_profile(db_pool, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": f"Profile with ID {profile_id} successfully deleted."}
