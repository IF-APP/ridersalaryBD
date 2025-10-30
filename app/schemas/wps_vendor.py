# app/schemas/wps_vendor.py
from app.schemas import BaseModel, Optional

class WPSVendorBase(BaseModel):
    vendor_name: str

class WPSVendorCreate(WPSVendorBase):
    pass

class WPSVendorUpdate(WPSVendorBase):
    pass

class WPSVendor(WPSVendorBase):
    wps_vendor_id: int
    
    class Config:
        from_attributes = True