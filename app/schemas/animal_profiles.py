from pydantic import BaseModel
from typing import Optional
from app.models import GenderEnum as Enum

class AnimalProfileBase(BaseModel):
    """
    Base schema for AnimalProfile(shared fields)
    """
    name: str
    species: str
    scientific_name: Optional[str] = None
    age: Optional[int]
    gender: Optional[Enum]
    
class AnimalProfileCreate(AnimalProfileBase):
    """
    Schema for creating an AnimalProfile
    """
    pass # this gets everything from animalprofilebase

class AnimalProfileResponse(AnimalProfileBase):
    """
    Schema for creating a new animal profile
    """
    id: int
    
    class Config:
        orm_mode = True # Allows the schema to understand ORM models
    