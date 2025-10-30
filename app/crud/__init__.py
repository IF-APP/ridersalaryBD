# app/crud/__init__.py
from app.crud.employee import (
    get_employee, get_employees, create_employee, 
    update_employee, delete_employee
)
from app.crud.partner import (
    get_partner, get_partners, create_partner,
    update_partner, delete_partner
)
from app.crud.wps_vendor import (
    get_wps_vendor, get_wps_vendors, create_wps_vendor,
    update_wps_vendor, delete_wps_vendor
)
from app.crud.weekly_trip import (
    get_weekly_trip, get_weekly_trips, get_weekly_trips_by_employee,
    create_weekly_trip, update_weekly_trip, delete_weekly_trip
)
from app.crud.deduction import (
    get_deduction, get_deductions, get_deductions_by_employee,
    create_deduction, update_deduction, delete_deduction
)
from app.crud.monthly_salary_report import (
    get_salary_report, get_salary_reports, get_salary_reports_by_employee,
    get_salary_reports_by_month, create_salary_report, update_salary_report, delete_salary_report
)