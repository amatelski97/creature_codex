from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Profiles as ProfilesModel
from app.schemas import ProfilesCreate, Profiles
from app import crud

router = APIRouter(
    prefix="/profiles/animal_profiles",  # Match Axios routes
    tags=["animal_profiles"],
)

# POST: Create a new profile
@router.post("/", response_model=Profiles)
def create_profiles(profile: ProfilesCreate, db: Session = Depends(get_db)):
    return crud.create_profiles(db=db, profile=profile)

# GET: Fetch all profiles
@router.get("/", response_model=list[Profiles])
def read_profiles(db: Session = Depends(get_db)):
    return crud.get_profiles(db=db)

# GET by ID: Fetch a single profile
@router.get("/{profile_id}", response_model=Profiles)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

# PUT: Update a profile by ID
@router.put("/{profile_id}", response_model=Profiles)
def update_profile(profile_id: int, profile: ProfilesCreate, db: Session = Depends(get_db)):
    updated_profile = crud.update_profile(db=db, profile_id=profile_id, profile=profile)
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
  
# DELETE: Delete a profile by ID
@router.delete("/{profile_id}", response_model=Profiles)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    return crud.delete_profile(db=db, profile_id=profile_id)

# GET: Search profiles
@router.get("/search", response_model=list[Profiles])
def search_profiles(
    name: str = Query(None),
    species: str = Query(None),
    scientific_name: str = Query(None),
    gender: str = Query(None),
    db: Session = Depends(get_db)
):
    return crud.search_profiles(db=db, name=name, species=species, scientific_name=scientific_name, gender=gender)