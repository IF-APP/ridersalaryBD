# app/schemas/__init__.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# Import all schemas
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from app.schemas.partner import Partner, PartnerCreate, PartnerUpdate
from app.schemas.wps_vendor import WPSVendor, WPSVendorCreate, WPSVendorUpdate
from app.schemas.weekly_trip import WeeklyTrip, WeeklyTripCreate, WeeklyTripUpdate
from app.schemas.deduction import Deduction, DeductionCreate, DeductionUpdate
from app.schemas.monthly_salary_report import MonthlySalaryReport, MonthlySalaryReportCreate, MonthlySalaryReportUpdate