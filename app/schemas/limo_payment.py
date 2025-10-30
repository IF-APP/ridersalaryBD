from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class LimoPaymentBase(BaseModel):
    limo_company: str
    limo_company_id: str
    captain_name: str
    captain_id: str
    payment_date: date
    payment_id: str
    payment_method: str
    total_driver_base_cost: Decimal
    total_driver_other_cost: Decimal = 0
    total_driver_payment: Decimal
    tips: Decimal = 0
    filename : str

class LimoPaymentCreate(LimoPaymentBase):
    pass

class LimoPaymentUpdate(LimoPaymentBase):
    pass

class LimoPayment(LimoPaymentBase):
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True