# app/schemas/employee.py
from app.schemas import BaseModel, Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    captain_id: Optional[str] = None
    name: str
    person_code: Optional[str] = None
    card_no: Optional[str] = None
    wps_vendor_id: Optional[int] = None
    designation: Optional[str] = None
    doj: Optional[date] = None
    partner_id: Optional[int] = None
    phone_no: Optional[str] = None
    emirates_id: Optional[str] = None
    passport_no: Optional[str] = None
    visa_status: Optional[str] = None
    training_fee: Optional[Decimal] = 0
    training_fee_deduction: Optional[Decimal] = 0
    status: Optional[str] = "Active"

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    employee_id: int
    
    class Config:
        from_attributes = True