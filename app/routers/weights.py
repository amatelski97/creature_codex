from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas.weights import WeightCreate, WeightResponse
from app.services.weights import (
    add_weight,
    get_weight_by_id,
    get_all_weights,
    update_weight,
    delete_weight,
)
from app.database import db_pool  # Assuming db_pool is an AsyncConnectionPool

router = APIRouter()

# POST: Add new weight
@router.post("/", response_model=WeightResponse, status_code=201)
async def create_weight(weight: WeightCreate):
    """
    Endpoint to add a new weight for an animal.
    """
    try:
        new_weight = await add_weight(db_pool, weight.animal_id, weight.weight, weight.record_date)
        return new_weight
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating weight: {str(e)}")

# GET: Fetch all weights
@router.get("/", response_model=List[WeightResponse])
async def fetch_all_weights():
    """
    Fetch all weight entries.
    """
    try:
        weights = await get_all_weights(db_pool)
        return weights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weights: {str(e)}")

# GET: Fetch a single weight by ID
@router.get("/{weight_id}", response_model=WeightResponse)
async def fetch_weight_by_id(weight_id: int):
    """
    Fetch a weight entry by its ID.
    """
    try:
        weight = await get_weight_by_id(db_pool, weight_id)
        if not weight:
            raise HTTPException(status_code=404, detail="Weight not found")
        return weight
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weight: {str(e)}")

# PUT: Update weight by ID
@router.put("/{weight_id}", response_model=dict)
async def update_weight_route(weight_id: int, weight: WeightCreate):
    """
    Update an existing weight by its ID and return raw dictionary.
    """
    try:
        updated_weight = await update_weight(db_pool, weight_id, weight.weight, weight.record_date)
        if not updated_weight:
            raise HTTPException(status_code=404, detail="Weight not found")
        return updated_weight  # Return the raw dictionary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating weight: {str(e)}")


# DELETE: Delete weight by ID
@router.delete("/{weight_id}", status_code=204)
async def delete_weight_route(weight_id: int):
    """
    Delete a weight entry by its ID.
    """
    try:
        success = await delete_weight(db_pool, weight_id)
        if not success:
            raise HTTPException(status_code=404, detail="Weight not found")
        return None  # Returning `204` status with no body
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting weight: {str(e)}")
