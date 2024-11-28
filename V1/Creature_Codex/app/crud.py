from sqlalchemy.orm import Session
from app.models import Profiles
from app.schemas import ProfilesCreate

def get_db():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_profiles(db: Session, profile: ProfilesCreate):
    db_profile = Profiles(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profiles(db: Session):
    return db.query(Profiles).all()

def get_profile(db: Session, profile_id: int):
    return db.query(Profiles).filter(Profiles.id == profile_id).first()

def update_profile(db: Session, profile_id: int, profile: ProfilesCreate):
    db_profile = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if db_profile:
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    db_profile = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if db_profile:
        db.delete(db_profile)
        db.commit()
    return db_profile

def search_profiles(db: Session, name: str = None, species: str = None, scientific_name: str = None, gender: str = None):
    query = db.query(Profiles)
    if name:
        query = query.filter(Profiles.name.ilike(f"%{name}%"))
    if species:
        query = query.filter(Profiles.species.ilike(f"%{species}%"))
    if scientific_name:
        query = query.filter(Profiles.scientific_name.ilike(f"%{scientific_name}%"))
    if gender:
        query = query.filter(Profiles.gender == gender)
    return query.all()