from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Weights
from app.schemas import WeightsCreate, WeightsRead

router = APIRouter(
    prefix="/weights",
    tags=["weights"],
)

@router.post("/", response_model=WeightsRead)
def create_weight(weight: WeightsCreate, db: Session = Depends(get_db)):
    db_weight = Weights(**weight.dict())
    db.add(db_weight)
    db.commit()
    db.refresh(db_weight)
    return db_weight

@router.get("/{weight_id}", response_model=WeightsRead)
def read_weight(weight_id: int, db: Session = Depends(get_db)):
    db_weight = db.query(Weights).filter(Weights.id == weight_id).first()
    if db_weight is None:
        raise HTTPException(status_code=404, detail="Weight log not found")
    return db_weight

@router.put("/{weight_id}", response_model=WeightsRead)
def update_weight(weight_id: int, weight: WeightsCreate, db: Session = Depends(get_db)):
    db_weight = db.query(Weights).filter(Weights.id == weight_id).first()
    if db_weight is None:
        raise HTTPException(status_code=404, detail="Weight log not found")
    for key, value in weight.dict().items():
        setattr(db_weight, key, value)
    db.commit()
    db.refresh(db_weight)
    return db_weight

@router.delete("/{weight_id}")
def delete_weight(weight_id: int, db: Session = Depends(get_db)):
    db_weight = db.query(Weights).filter(Weights.id == weight_id).first()
    if db_weight is None:
        raise HTTPException(status_code=404, detail="Weight log not found")
    db.delete(db_weight)
    db.commit()
    return {"detail": "Weight log deleted"}
