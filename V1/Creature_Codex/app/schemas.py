from pydantic import BaseModel
from pydantic import BaseModel
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class ProfilesCreate(BaseModel):
    name: str
    age: int
    species: str
    scientific_name: str
    gender: GenderEnum  # Enforce enum validation

class ProfilesBase(BaseModel):
    name: str
    age: int
    species: str
    scientific_name: str
    gender: str

class ProfilesCreate(ProfilesBase):
    pass

class Profiles(ProfilesBase):
    id: int

    class Config:
        from_attributes = True  # Update for Pydantic v2