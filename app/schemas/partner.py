# app/schemas/partner.py
from app.schemas import BaseModel, Optional

class PartnerBase(BaseModel):
    partner_name: str
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None

class PartnerCreate(PartnerBase):
    pass

class PartnerUpdate(PartnerBase):
    pass

class Partner(PartnerBase):
    partner_id: int
    
    class Config:
        from_attributes = True