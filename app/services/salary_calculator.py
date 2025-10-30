# app/services/salary_calculator.py
from sqlalchemy.orm import Session
from datetime import datetime
from app.crud import weekly_trip as weekly_trip_crud
from app.crud import deduction as deduction_crud
from app.crud import employee as employee_crud
from app.crud import monthly_salary_report as salary_report_crud
from decimal import Decimal

def calculate_monthly_salary(db: Session, employee_id: int, month_year: str):
    # Get employee
    employee = employee_crud.get_employee(db, employee_id)
    if not employee:
        return {"error": "Employee not found"}
    
    # Get all weekly trips for the month
    weekly_trips = weekly_trip_crud.get_weekly_trips_by_employee(db, employee_id)
    
    # Filter trips for the specific month (simplified logic)
    month_trips = [trip for trip in weekly_trips if trip.week_start_date.strftime("%b-%Y") == month_year]
    
    # Calculate totals
    total_hours = sum(trip.total_working_hours or Decimal('0') for trip in month_trips)
    total_orders = sum(trip.total_orders or 0 for trip in month_trips)
    actual_order_pay = sum(trip.actual_order_pay or Decimal('0') for trip in month_trips)
    total_excess_pay = sum(trip.excess_pay or Decimal('0') for trip in month_trips)
    total_cod = sum(trip.cod_collected or Decimal('0') for trip in month_trips)
    
    # Calculate gross pay
    gross_pay = actual_order_pay + total_excess_pay
    
    # Get deductions for the month
    deductions = deduction_crud.get_deductions_by_employee(db, employee_id)
    month_deductions = [ded for ded in deductions if ded.monthstart_date.strftime("%b-%Y") == month_year]
    
    # Calculate total deductions
    vendor_fee = sum(ded.vendor_fee or Decimal('0') for ded in month_deductions)
    traffic_fine = sum(ded.traffic_fine or Decimal('0') for ded in month_deductions)
    loan_fine = sum(ded.loan_fine or Decimal('0') for ded in month_deductions)
    training_fee = sum(ded.training_fee or Decimal('0') for ded in month_deductions)
    
    total_deductions = vendor_fee + traffic_fine + loan_fine + training_fee
    
    # Calculate net salary
    net_salary = gross_pay - total_deductions
    
    return {
        "employee_id": employee_id,
        "month_year": month_year,
        "total_working_hours": total_hours,
        "no_of_days": len(month_trips) * 7,  # Approximate
        "total_orders": total_orders,
        "actual_order_pay": actual_order_pay,
        "total_excess_pay": total_excess_pay,
        "gross_pay": gross_pay,
        "total_cod": total_cod,
        "vendor_fee": vendor_fee,
        "traffic_fine": traffic_fine,
        "loan_fine": loan_fine,
        "training_fee": training_fee,
        "net_salary": net_salary,
        "remarks": f"Auto-generated for {month_year}"
    }