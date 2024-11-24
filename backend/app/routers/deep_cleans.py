from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DeepClean
from app.schemas import DeepCleanCreate, DeepCleanRead

router = APIRouter(
    prefix="/deep_cleans",
    tags=["deep_cleans"],
)

@router.post("/", response_model=DeepCleanRead)
def create_deep_clean(deep_clean: DeepCleanCreate, db: Session = Depends(get_db)):
    db_deep_clean = DeepClean(**deep_clean.dict())
    db.add(db_deep_clean)
    db.commit()
    db.refresh(db_deep_clean)
    return db_deep_clean

@router.get("/{deep_clean_id}", response_model=DeepCleanRead)
def read_deep_clean(deep_clean_id: int, db: Session = Depends(get_db)):
    db_deep_clean = db.query(DeepClean).filter(DeepClean.id == deep_clean_id).first()
    if db_deep_clean is None:
        raise HTTPException(status_code=404, detail="Deep clean log not found")
    return db_deep_clean

@router.put("/{deep_clean_id}", response_model=DeepCleanRead)
def update_deep_clean(deep_clean_id: int, deep_clean: DeepCleanCreate, db: Session = Depends(get_db)):
    db_deep_clean = db.query(DeepClean).filter(DeepClean.id == deep_clean_id).first()
    if db_deep_clean is None:
        raise HTTPException(status_code=404, detail="Deep clean log not found")
    for key, value in deep_clean.dict().items():
        setattr(db_deep_clean, key, value)
    db.commit()
    db.refresh(db_deep_clean)
    return db_deep_clean

@router.delete("/{deep_clean_id}")
def delete_deep_clean(deep_clean_id: int, db: Session = Depends(get_db)):
    db_deep_clean = db.query(DeepClean).filter(DeepClean.id == deep_clean_id).first()
    if db_deep_clean is None:
        raise HTTPException(status_code=404, detail="Deep clean log not found")
    db.delete(db_deep_clean)
    db.commit()
    return {"detail": "Deep clean log deleted"}