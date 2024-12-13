from pydantic import BaseModel
from datetime import date
from typing import Optional


class WeightBase(BaseModel):
    """
    Base schema for Weights (shared fields).
    """
    animal_id: int
    weight: float
    record_date: date  # ISO format for the date


class WeightCreate(WeightBase):
    """
    Schema for creating a new weight record.
    """
    pass  # Inherits all fields from WeightBase


class WeightResponse(WeightBase):
    """
    Schema for returning a weight record.
    """
    id: int  # The unique ID of the weight record
    
    class Config:
        from_attributes = True
        orm_mode = True  # Ensures compatibility with ORM objects
        allow_population_by_field_name = True  # Enable using aliases if needed

class WeightUpdate(BaseModel):
    """
    Schema for updating weight records.
    """
    animal_id: Optional[int] = None
    weight: Optional[float] = None
    record_date: Optional[date] = None

    class Config:
        from_attributes = True  # Enables parsing raw database rows
