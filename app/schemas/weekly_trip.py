from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class WeeklyTripBase(BaseModel):
    # employee_id: int
    employee_id: Optional[int] = None
    week_start_date: date
    week_end_date: date
    total_working_hours: Optional[Decimal] = 0
    total_orders: Optional[int] = 0
    actual_order_pay: Optional[Decimal] = 0
    excess_pay: Optional[Decimal] = 0
    cod_collected: Optional[Decimal] = 0
    upload_batch_id: Optional[int] = None

class WeeklyTripCreate(WeeklyTripBase):
    pass

class WeeklyTripUpdate(WeeklyTripBase):
    pass

class WeeklyTrip(WeeklyTripBase):
    trip_id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True