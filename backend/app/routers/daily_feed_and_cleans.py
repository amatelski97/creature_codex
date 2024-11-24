from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DailyFeedAndClean, DailyFeedLog
from app.schemas import DailyFeedAndCleanCreate, DailyFeedAndCleanRead
from datetime import datetime, timedelta
import csv
import os

router = APIRouter(
    prefix="/daily_feed_and_cleans",
    tags=["daily_feed_and_cleans"],
)

# Create a new daily feed and clean log
@router.post("/", response_model=DailyFeedAndCleanRead)
def create_daily_feed_and_clean(daily_feed_and_clean: DailyFeedAndCleanCreate, db: Session = Depends(get_db)):
    db_daily_feed_and_clean = DailyFeedAndClean(**daily_feed_and_clean.dict())
    db.add(db_daily_feed_and_clean)
    db.commit()
    db.refresh(db_daily_feed_and_clean)
    return db_daily_feed_and_clean

# Read a daily feed and clean log by ID
@router.get("/{daily_feed_and_clean_id}", response_model=DailyFeedAndCleanRead)
def read_daily_feed_and_clean(daily_feed_and_clean_id: int, db: Session = Depends(get_db)):
    db_daily_feed_and_clean = db.query(DailyFeedAndClean).filter(DailyFeedAndClean.id == daily_feed_and_clean_id).first()
    if db_daily_feed_and_clean is None:
        raise HTTPException(status_code=404, detail="Daily feed and clean log not found")
    return db_daily_feed_and_clean

# Update a daily feed and clean log by ID
@router.put("/{daily_feed_and_clean_id}", response_model=DailyFeedAndCleanRead)
def update_daily_feed_and_clean(daily_feed_and_clean_id: int, daily_feed_and_clean: DailyFeedAndCleanCreate, db: Session = Depends(get_db)):
    db_daily_feed_and_clean = db.query(DailyFeedAndClean).filter(DailyFeedAndClean.id == daily_feed_and_clean_id).first()
    if db_daily_feed_and_clean is None:
        raise HTTPException(status_code=404, detail="Daily feed and clean log not found")
    for key, value in daily_feed_and_clean.dict().items():
        setattr(db_daily_feed_and_clean, key, value)
    db.commit()
    db.refresh(db_daily_feed_and_clean)
    return db_daily_feed_and_clean

# Delete a daily feed and clean log by ID
@router.delete("/{daily_feed_and_clean_id}")
def delete_daily_feed_and_clean(daily_feed_and_clean_id: int, db: Session = Depends(get_db)):
    db_daily_feed_and_clean = db.query(DailyFeedAndClean).filter(DailyFeedAndClean.id == daily_feed_and_clean_id).first()
    if db_daily_feed_and_clean is None:
        raise HTTPException(status_code=404, detail="Daily feed and clean log not found")
    db.delete(db_daily_feed_and_clean)
    db.commit()
    return {"detail": "Daily feed and clean log deleted"}

# Reset daily feed and clean logs for today
@router.post("/reset")
def reset_daily_feed_and_clean(db: Session = Depends(get_db)):
    yesterday = datetime.now() - timedelta(days=1)
    daily_feed_and_cleans = db.query(DailyFeedAndClean).filter(DailyFeedAndClean.date == yesterday.date()).all()
    if not daily_feed_and_cleans:
        raise HTTPException(status_code=404, detail="No daily feed and clean logs found for yesterday")
    
    # Save the data from yesterday to the DailyFeedLog table
    for log in daily_feed_and_cleans:
        db_daily_feed_log = DailyFeedLog(
            animal_id=log.animal_id,
            animal_name=log.animal_name,
            date=log.date,
            prepped=log.prepped,
            fed=log.fed,
            cleaned=log.cleaned,
            leftovers=log.leftovers,
            water=log.water,
            poop=log.poop,
            notes=log.notes,
            staff_only=log.staff_only,
            fed_by=log.fed_by
        )
        db.add(db_daily_feed_log)
    
    db.commit()
    
    # Reset the table for today
    db.query(DailyFeedAndClean).delete()
    db.commit()
    return {"detail": "Daily feed and clean logs reset for today"}
