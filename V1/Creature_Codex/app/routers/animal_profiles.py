from fastapi import APIRouter, HTTPException, Query, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Profiles as ProfilesModel
from app.schemas import ProfilesCreate, Profiles
from app import crud
import csv

router = APIRouter(
    prefix="/profiles",  # Match Axios routes
    tags=["animal_profiles"],
)

# POST: Create a new profile
@router.post("/", response_model=Profiles)
async def create_profiles(profile: ProfilesCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_profiles(db=db, profile=profile)

# GET: Fetch all profiles
@router.get("/", response_model=list[Profiles])
async def read_profiles(db: AsyncSession = Depends(get_db)):
    return await crud.get_profiles(db=db)

# Add a new route for uploading CSV files
@router.post("/upload_csv/")
async def upload_csv(file: UploadFile, db: AsyncSession = Depends(get_db)):
    try:
        contents = await file.read()
        csv_data = csv.DictReader(contents.decode("utf-8").splitlines())

        profiles = []
        for row in csv_data:
            age = int(row["age"]) if row["age"] and row["age"].isdigit() else None
            gender = row["gender"].upper() if row["gender"].upper() in ["MALE", "FEMALE", "OTHER"] else "OTHER"
            profiles.append(
                ProfilesCreate(
                    name=row["name"],
                    species=row["species"],
                    scientific_name=row["scientific_name"],
                    age=age,
                    gender=gender,  # Validate gender
                )
            )

        for profile in profiles:
            await crud.create_profiles(db, profile)

        return {"message": "CSV uploaded successfully"}
    except Exception as e:
        print(f"Error during CSV upload: {e}")  # Log the error
        raise HTTPException(status_code=500, detail="CSV upload failed")
    
# Other routes for CRUD operations remain unchanged
@router.post("/", response_model=Profiles)
async def create_profile(profile: ProfilesCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_profiles(db=db, profile=profile)