from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from enum import Enum
from app.database import Base  # Use Base from app.database

class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Profiles(Base):
    __tablename__ = "animal_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String)
    scientific_name = Column(String)
    age = Column(Integer)
    gender = Column(SqlEnum(GenderEnum, name="gender_enum", native_enum=False, create_type=False))

    # relationships (optional)
