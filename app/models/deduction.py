# app/models/deduction.py
from sqlalchemy import Column, String, Integer, Date, DECIMAL, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from app.database import Base

class Deduction(Base):
    __tablename__ = "deductions"

    deduction_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    monthstart_date = Column(Date, nullable=False)
    vendor_fee = Column(DECIMAL(10, 2), default=0)
    traffic_fine = Column(DECIMAL(10, 2), default=0)
    loan_fine = Column(DECIMAL(10, 2), default=0)
    training_fee = Column(DECIMAL(10, 2), default=0)
    others = Column(DECIMAL(10, 2), default=0)
    remarks = Column(TEXT)

    employee = relationship("Employee", back_populates="deductions")