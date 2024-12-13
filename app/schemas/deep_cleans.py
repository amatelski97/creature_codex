from pydantic import BaseModel
from datetime import date

class DeepCleanBase(BaseModel):
    animal_id: int
    clean_date: date
    cleaner_name: str
    notes: str

class DeepCleanCreate(DeepCleanBase):
    """
    Schema for creating a new deep clean entry.
    """
    pass

class DeepCleanResponse(DeepCleanBase):
    id: int

    class Config:
        from_attributes = True  # Enables parsing raw database rows
