# app/models/wps_vendor.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class WPSVendor(Base):
    __tablename__ = "wps_vendors"

    wps_vendor_id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(100), nullable=False)

    employees = relationship("Employee", back_populates="wps_vendor")