# app/crud/wps_vendor.py
from sqlalchemy.orm import Session
from app.models.wps_vendor import WPSVendor
from app.schemas.wps_vendor import WPSVendorCreate, WPSVendorUpdate
from typing import List, Optional

def get_wps_vendor(db: Session, wps_vendor_id: int) -> Optional[WPSVendor]:
    return db.query(WPSVendor).filter(WPSVendor.wps_vendor_id == wps_vendor_id).first()

def get_wps_vendors(db: Session, skip: int = 0, limit: int = 100) -> List[WPSVendor]:
    return db.query(WPSVendor).offset(skip).limit(limit).all()

def create_wps_vendor(db: Session, wps_vendor: WPSVendorCreate) -> WPSVendor:
    db_wps_vendor = WPSVendor(**wps_vendor.dict())
    db.add(db_wps_vendor)
    db.commit()
    db.refresh(db_wps_vendor)
    return db_wps_vendor

def update_wps_vendor(db: Session, wps_vendor_id: int, wps_vendor: WPSVendorUpdate) -> Optional[WPSVendor]:
    db_wps_vendor = db.query(WPSVendor).filter(WPSVendor.wps_vendor_id == wps_vendor_id).first()
    if db_wps_vendor:
        for key, value in wps_vendor.dict(exclude_unset=True).items():
            setattr(db_wps_vendor, key, value)
        db.commit()
        db.refresh(db_wps_vendor)
    return db_wps_vendor

def delete_wps_vendor(db: Session, wps_vendor_id: int) -> bool:
    db_wps_vendor = db.query(WPSVendor).filter(WPSVendor.wps_vendor_id == wps_vendor_id).first()
    if db_wps_vendor:
        db.delete(db_wps_vendor)
        db.commit()
        return True
    return False