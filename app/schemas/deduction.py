# app/schemas/deduction.py
from app.schemas import BaseModel, Optional
from datetime import date
from decimal import Decimal

class DeductionBase(BaseModel):
    employee_id: Optional[int] = None
    monthstart_date: date
    vendor_fee: Optional[Decimal] = 0
    traffic_fine: Optional[Decimal] = 0
    loan_fine: Optional[Decimal] = 0
    training_fee: Optional[Decimal] = 0
    others: Optional[Decimal] = 0
    remarks: Optional[str] = None

class DeductionCreate(DeductionBase):
    pass

class DeductionUpdate(DeductionBase):
    pass

class Deduction(DeductionBase):
    deduction_id: int
    
    class Config:
        from_attributes = True