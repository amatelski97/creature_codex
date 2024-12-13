from pydantic import BaseModel
from typing import Optional
from app.models import GenderEnum, AnimalCategory

# Base schema for AnimalProfiles (shared fields)
class AnimalProfileBase(BaseModel):
    """
    Base schema for AnimalProfiles.
    """
    name: str
    species: str
    scientific_name: Optional[str] = None
    age: Optional[int] = None
    gender: GenderEnum
    category: AnimalCategory

# Schema for creating an AnimalProfile
class AnimalProfileCreate(AnimalProfileBase):
    """
    Schema for creating an AnimalProfile.
    """
    pass  # Inherits fields from AnimalProfileBase

# Schema for responding with AnimalProfile
class AnimalProfileResponse(AnimalProfileBase):
    """
    Schema for returning an AnimalProfile.
    """
    id: int  # ID is included in the response schema
    latest_weight: Optional[float] = None
    latest_record_date: Optional[str] = None  # Dates are ISO formatted strings

    class Config:
        from_attributes = True  # For compatibility with Psycopg or raw DB results
