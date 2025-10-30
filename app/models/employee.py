# app/models/employee.py
from sqlalchemy import Column, String, Integer, Date, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class EmployeeStatus(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    captain_id = Column(String(50))
    name = Column(String(100), nullable=False)
    person_code = Column(String(50))
    card_no = Column(String(50))
    wps_vendor_id = Column(Integer, ForeignKey('wps_vendors.wps_vendor_id'))
    designation = Column(String(50))
    doj = Column(Date)  # Date of joining
    partner_id = Column(Integer, ForeignKey('partners.partner_id'))
    phone_no = Column(String(20))
    emirates_id = Column(String(50))
    passport_no = Column(String(50))
    visa_status = Column(String(50))
    training_fee = Column(DECIMAL(10, 2), default=0)
    training_fee_deduction = Column(DECIMAL(10, 2), default=0)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.Active)

    # Relationships
    partner = relationship("Partner", back_populates="employees")
    wps_vendor = relationship("WPSVendor", back_populates="employees")
    weekly_trips = relationship("WeeklyTrip", back_populates="employee")
    deductions = relationship("Deduction", back_populates="employee")
    # salary_reports = relationship("MonthlySalaryReport", back_populates="employee")