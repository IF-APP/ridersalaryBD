from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SettingsBase(BaseModel):
    company_name: str
    training_fee: float
    cutoff_date: int
    email_notifications: bool
    auto_generate_reports: bool
    currency: str

class SettingsUpdate(BaseModel):
    company_name: Optional[str] = None
    training_fee: Optional[float] = None
    cutoff_date: Optional[int] = None
    email_notifications: Optional[bool] = None
    auto_generate_reports: Optional[bool] = None

class SettingsResponse(SettingsBase):
    id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: str
    role: str  # "Administrator", "Manager", "Staff"
    password: str  

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    status: str
    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    user: str
    action: str
    timestamp: datetime
    class Config:
        from_attributes = True