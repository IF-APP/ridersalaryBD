# app/models/partner.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class Partner(Base):
    __tablename__ = "partners"

    partner_id = Column(Integer, primary_key=True, index=True)
    partner_name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    contact_email = Column(String(100))

    employees = relationship("Employee", back_populates="partner")