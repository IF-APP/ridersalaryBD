from app.schemas import BaseModel, Optional
from datetime import datetime, date
from decimal import Decimal
from pydantic import Field

class MonthlySalaryReportBase(BaseModel):
    careem_captain_id: Optional[str] = None
    person_code: Optional[str] = None
    card_no: Optional[str] = None
    designation: Optional[str] = None
    doj: Optional[date] = None
    name: Optional[str] = None
    total_working_hours: Optional[float] = Field(0, ge=0)
    no_of_days: Optional[int] = Field(0, ge=0)
    total_orders: Optional[int] = Field(0, ge=0)
    actual_order_pay: Optional[float] = Field(0, ge=0)
    total_excess_pay: float = 0
    gross_pay: float = 0
    total_cod: float = 0
    vendor_fee: float = 0
    traffic_fine: float = 0
    loan_fine: float = 0
    training_fee: float = 0
    net_salary: float = 0
    remarks: Optional[str] = None
    month_year: Optional[str] = None

class MonthlySalaryReportCreate(MonthlySalaryReportBase):
    pass

class MonthlySalaryReportUpdate(MonthlySalaryReportBase):
    pass

class MonthlySalaryReport(MonthlySalaryReportBase):
    report_id: int
    generated_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True