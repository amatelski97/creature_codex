from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud
from ..database import get_db

# This section imports necessary modules and dependencies


# Create a new router instance for training logs
router = APIRouter(
    prefix="/training_logs",
    tags=["training_logs"],
    responses={404: {"description": "Not found"}},
)

# This endpoint retrieves all training logs
@router.get("/", response_model=List[schemas.TrainingLog])
def read_training_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    training_logs = crud.get_training_logs(db, skip=skip, limit=limit)
    return training_logs

# This endpoint retrieves a specific training log by ID
@router.get("/{training_log_id}", response_model=schemas.TrainingLog)
def read_training_log(training_log_id: int, db: Session = Depends(get_db)):
    db_training_log = crud.get_training_log(db, training_log_id=training_log_id)
    if db_training_log is None:
        raise HTTPException(status_code=404, detail="Training log not found")
    return db_training_log

# This endpoint creates a new training log
@router.post("/", response_model=schemas.TrainingLog)
def create_training_log(training_log: schemas.TrainingLogCreate, db: Session = Depends(get_db)):
    return crud.create_training_log(db=db, training_log=training_log)

# This endpoint updates an existing training log
@router.put("/{training_log_id}", response_model=schemas.TrainingLog)
def update_training_log(training_log_id: int, training_log: schemas.TrainingLogUpdate, db: Session = Depends(get_db)):
    db_training_log = crud.get_training_log(db, training_log_id=training_log_id)
    if db_training_log is None:
        raise HTTPException(status_code=404, detail="Training log not found")
    return crud.update_training_log(db=db, training_log=training_log, training_log_id=training_log_id)

# This endpoint deletes a training log by ID
@router.delete("/{training_log_id}", response_model=schemas.TrainingLog)
def delete_training_log(training_log_id: int, db: Session = Depends(get_db)):
    db_training_log = crud.get_training_log(db, training_log_id=training_log_id)
    if db_training_log is None:
        raise HTTPException(status_code=404, detail="Training log not found")
    return crud.delete_training_log(db=db, training_log_id=training_log_id)