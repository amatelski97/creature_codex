from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date

from app.schemas.deep_cleans import DeepCleanCreate, DeepCleanResponse
from app.services.deep_cleans import (
    add_deep_clean,
    get_deep_clean_by_id,
    get_all_deep_cleans,
    update_deep_clean,
    delete_deep_clean,
)
from app.database import db_pool  # Assuming db_pool is an AsyncConnectionPool

router = APIRouter()

# POST: Add new deep clean
@router.post("/", response_model=DeepCleanResponse, status_code=201)
async def create_deep_clean(clean_data: DeepCleanCreate):
    """
    Endpoint to add a new deep clean entry for an animal.
    """
    try:
        new_clean = await add_deep_clean(
            db_pool,
            {
                "animal_id": clean_data.animal_id,
                "clean_date": clean_data.clean_date,
                "cleaner_name": clean_data.cleaner_name,
                "notes": clean_data.notes,
            },
        )
        return new_clean
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating deep clean: {str(e)}")

# GET: Fetch all deep cleans
@router.get("/", response_model=List[DeepCleanResponse])
async def fetch_all_deep_cleans(animal_id: int = None):
    """
    Fetch all deep clean entries, optionally filtered by animal ID.
    """
    try:
        cleans = await get_all_deep_cleans(db_pool, animal_id)
        return cleans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching deep cleans: {str(e)}")

# GET: Fetch a single deep clean by ID
@router.get("/{clean_id}", response_model=DeepCleanResponse)
async def fetch_deep_clean_by_id(clean_id: int):
    """
    Fetch a deep clean entry by its ID.
    """
    try:
        clean = await get_deep_clean_by_id(db_pool, clean_id)
        if not clean:
            raise HTTPException(status_code=404, detail="Deep clean not found")
        return clean
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching deep clean: {str(e)}")

# PUT: Update deep clean by ID
@router.put("/{clean_id}", response_model=DeepCleanResponse)
async def update_deep_clean_route(clean_id: int, clean_data: DeepCleanCreate):
    """
    Update an existing deep clean entry by its ID.
    """
    try:
        updated_clean = await update_deep_clean(
            db_pool,
            clean_id,
            {
                "clean_date": clean_data.clean_date,
                "cleaner_name": clean_data.cleaner_name,
                "notes": clean_data.notes,
            },
        )
        if not updated_clean:
            raise HTTPException(status_code=404, detail="Deep clean not found")
        return updated_clean
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating deep clean: {str(e)}")

# DELETE: Delete deep clean by ID
@router.delete("/{clean_id}", status_code=204)
async def delete_deep_clean_route(clean_id: int):
    """
    Delete a deep clean entry by its ID.
    """
    try:
        success = await delete_deep_clean(db_pool, clean_id)
        if not success:
            raise HTTPException(status_code=404, detail="Deep clean not found")
        return None  # Returning `204` status with no body
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting deep clean: {str(e)}")
