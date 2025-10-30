from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func
from app.database import Base

class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), default="RiderApp Management")
    training_fee = Column(Float, default=500.00)
    cutoff_date = Column(Integer, default=3)  # Day of month
    email_notifications = Column(Boolean, default=True)
    auto_generate_reports = Column(Boolean, default=True)
    currency = Column(String(10), default="AED")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100))
    action = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())