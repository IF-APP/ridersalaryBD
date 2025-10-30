# app/routes/__init__.py
from app.routes.employees import router as employees_router
from app.routes.partners import router as partners_router
from app.routes.wps_vendors import router as wps_vendors_router
from app.routes.weekly_trips import router as weekly_trips_router
from app.routes.deductions import router as deductions_router
from app.routes.monthly_salary_reports import router as monthly_salary_reports_router