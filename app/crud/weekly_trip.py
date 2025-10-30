# app/crud/weekly_trip.py
from sqlalchemy.orm import Session
from app.models.weekly_trip import WeeklyTrip
from app.schemas.weekly_trip import WeeklyTripCreate, WeeklyTripUpdate
from typing import List, Optional
from datetime import datetime

def get_weekly_trip(db: Session, trip_id: int) -> Optional[WeeklyTrip]:
    return db.query(WeeklyTrip).filter(WeeklyTrip.trip_id == trip_id).first()

def get_weekly_trips(db: Session, skip: int = 0, limit: int = 100) -> List[WeeklyTrip]:
    return db.query(WeeklyTrip).offset(skip).limit(limit).all()

def get_weekly_trips_by_employee(db: Session, employee_id: int) -> List[WeeklyTrip]:
    return db.query(WeeklyTrip).filter(WeeklyTrip.employee_id == employee_id).all()

def create_weekly_trip(db: Session, weekly_trip: WeeklyTripCreate) -> WeeklyTrip:
    db_weekly_trip = WeeklyTrip(**weekly_trip.dict(), created_at=datetime.now())
    db.add(db_weekly_trip)
    db.commit()
    db.refresh(db_weekly_trip)
    return db_weekly_trip

def update_weekly_trip(db: Session, trip_id: int, weekly_trip: WeeklyTripUpdate) -> Optional[WeeklyTrip]:
    db_weekly_trip = db.query(WeeklyTrip).filter(WeeklyTrip.trip_id == trip_id).first()
    if db_weekly_trip:
        for key, value in weekly_trip.dict(exclude_unset=True).items():
            setattr(db_weekly_trip, key, value)
        db.commit()
        db.refresh(db_weekly_trip)
    return db_weekly_trip

def delete_weekly_trip(db: Session, trip_id: int) -> bool:
    db_weekly_trip = db.query(WeeklyTrip).filter(WeeklyTrip.trip_id == trip_id).first()
    if db_weekly_trip:
        db.delete(db_weekly_trip)
        db.commit()
        return True
    return False