# app/routes/wps_vendors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.wps_vendor import WPSVendor, WPSVendorCreate, WPSVendorUpdate
from app.crud import wps_vendor as crud

router = APIRouter(prefix="/wps-vendors", tags=["wps-vendors"])

@router.post("/", response_model=WPSVendor)
def create_wps_vendor(wps_vendor: WPSVendorCreate, db: Session = Depends(get_db)):
    return crud.create_wps_vendor(db=db, wps_vendor=wps_vendor)

@router.get("/", response_model=list[WPSVendor])
def read_wps_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wps_vendors = crud.get_wps_vendors(db, skip=skip, limit=limit)
    return wps_vendors

@router.get("/{wps_vendor_id}", response_model=WPSVendor)
def read_wps_vendor(wps_vendor_id: int, db: Session = Depends(get_db)):
    db_wps_vendor = crud.get_wps_vendor(db, wps_vendor_id=wps_vendor_id)
    if db_wps_vendor is None:
        raise HTTPException(status_code=404, detail="WPS Vendor not found")
    return db_wps_vendor

@router.put("/{wps_vendor_id}", response_model=WPSVendor)
def update_wps_vendor(wps_vendor_id: int, wps_vendor: WPSVendorUpdate, db: Session = Depends(get_db)):
    db_wps_vendor = crud.update_wps_vendor(db, wps_vendor_id=wps_vendor_id, wps_vendor=wps_vendor)
    if db_wps_vendor is None:
        raise HTTPException(status_code=404, detail="WPS Vendor not found")
    return db_wps_vendor

@router.delete("/{wps_vendor_id}")
def delete_wps_vendor(wps_vendor_id: int, db: Session = Depends(get_db)):
    success = crud.delete_wps_vendor(db, wps_vendor_id=wps_vendor_id)
    if not success:
        raise HTTPException(status_code=404, detail="WPS Vendor not found")
    return {"message": "WPS Vendor deleted successfully"}