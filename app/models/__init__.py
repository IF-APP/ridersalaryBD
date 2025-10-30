# app/models/__init__.py
from sqlalchemy import Column, Integer, String, DateTime, func

class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # app/models/__init__.py
from app.models.employee import Employee
from app.models.partner import Partner
from app.models.wps_vendor import WPSVendor
from app.models.weekly_trip import WeeklyTrip
from app.models.deduction import Deduction
from app.models.monthly_salary_report import MonthlySalaryReport