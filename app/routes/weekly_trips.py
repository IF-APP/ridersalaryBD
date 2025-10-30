# app/routes/weekly_trips.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.weekly_trip import WeeklyTrip, WeeklyTripCreate, WeeklyTripUpdate
from app.crud import weekly_trip as crud

router = APIRouter(prefix="/weekly-trips", tags=["weekly-trips"])

@router.post("/", response_model=WeeklyTrip)
def create_weekly_trip(weekly_trip: WeeklyTripCreate, db: Session = Depends(get_db)):
    return crud.create_weekly_trip(db=db, weekly_trip=weekly_trip)

@router.get("/", response_model=list[WeeklyTrip])
def read_weekly_trips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    weekly_trips = crud.get_weekly_trips(db, skip=skip, limit=limit)
    return weekly_trips

@router.get("/employee/{employee_id}", response_model=list[WeeklyTrip])
def read_weekly_trips_by_employee(employee_id: int, db: Session = Depends(get_db)):
    weekly_trips = crud.get_weekly_trips_by_employee(db, employee_id=employee_id)
    return weekly_trips

@router.get("/{trip_id}", response_model=WeeklyTrip)
def read_weekly_trip(trip_id: int, db: Session = Depends(get_db)):
    db_weekly_trip = crud.get_weekly_trip(db, trip_id=trip_id)
    if db_weekly_trip is None:
        raise HTTPException(status_code=404, detail="Weekly trip not found")
    return db_weekly_trip

@router.put("/{trip_id}", response_model=WeeklyTrip)
def update_weekly_trip(trip_id: int, weekly_trip: WeeklyTripUpdate, db: Session = Depends(get_db)):
    db_weekly_trip = crud.update_weekly_trip(db, trip_id=trip_id, weekly_trip=weekly_trip)
    if db_weekly_trip is None:
        raise HTTPException(status_code=404, detail="Weekly trip not found")
    return db_weekly_trip

@router.delete("/{trip_id}")
def delete_weekly_trip(trip_id: int, db: Session = Depends(get_db)):
    success = crud.delete_weekly_trip(db, trip_id=trip_id)
    if not success:
        raise HTTPException(status_code=404, detail="Weekly trip not found")
    return {"message": "Weekly trip deleted successfully"}

@router.post("/upload/")
async def upload_weekly_trips(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files are allowed")
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "total_records": 0,
            "valid_records": 0,
            "errors": 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")