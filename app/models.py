from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from enum import Enum
from app.database import Base  # Use Base from database

class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    
# Define Profiles table

class AnimalProfiles(Base):
    __tablename__="animal_profiles" # Table name matches the purpose
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, index=True, nullable=False)  # Required field
    species = Column(String, nullable=False)  # Required field
    scientific_name = Column(String, nullable=True)  # Optional field
    age = Column(Integer, nullable=True)  # Optional field
    gender = Column(
        SqlEnum(GenderEnum, name="gender_enum", native_enum=False, create_type=False)
    )  # Enum for gender with a defined type