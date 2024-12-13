from enum import Enum
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


# Define enums for animal attributes
class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class AnimalCategory(str, Enum):
    MAMMAL = "MAMMAL"
    BIRD = "BIRD"
    REPTILE = "REPTILE"
    AMPHIBIAN = "AMPHIBIAN"
    INVERTEBRATE = "INVERTEBRATE"


# Pydantic models for Animal Profiles and Weights
class AnimalProfile(BaseModel):
    """
    Represents an animal profile with basic information and latest stats.
    """
    id: int
    name: str
    species: str
    scientific_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    category: Optional[AnimalCategory] = None
    latest_weight: Optional[float] = None
    latest_record_date: Optional[date] = None  # Use `date` for proper validation

    class Config:
        from_attributes = True  # Replaces `orm_mode`


class Weight(BaseModel):
    """
    Represents a weight entry for an animal.
    """
    id: int
    animal_id: int
    weight: float
    record_date: date  # Use `date` for proper validation

    class Config:
        from_attributes = True  # Replaces `orm_mode`
        
class deep_clean(BaseModel):
    """
    Represents a deep clean entry for an animal.
    """
    id: int
    animal_id: int
    clean_date: date  # Use `date` for proper validation
    cleaner_name: str
    notes: str

    class Config:
        from_attributes = True  # Replaces `orm_mode`
