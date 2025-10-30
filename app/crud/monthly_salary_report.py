# app/crud/monthly_salary_report.py
from sqlalchemy.orm import Session, joinedload
from app.models.monthly_salary_report import MonthlySalaryReport
from app.schemas.monthly_salary_report import MonthlySalaryReportCreate, MonthlySalaryReportUpdate
from typing import List, Optional
from datetime import datetime
from app.models.limo_payment import LimoPayment
from app.models.employee import Employee
from app.models.deduction import Deduction
from sqlalchemy import extract

def get_salary_report(db: Session, report_id: int) -> Optional[MonthlySalaryReport]:
    return db.query(MonthlySalaryReport).options(joinedload(MonthlySalaryReport.employee)).filter(MonthlySalaryReport.report_id == report_id).first()

def get_salary_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MonthlySalaryReport).offset(skip).limit(limit).all()

def get_salary_reports_by_employee(db: Session, employee_id: int) -> List[MonthlySalaryReport]:
    return db.query(MonthlySalaryReport)
def get_salary_reports_by_month(db: Session, month_year: str) -> List[MonthlySalaryReport]:
    return db.query(MonthlySalaryReport)

def create_salary_report(db: Session, salary_report: MonthlySalaryReportCreate) -> MonthlySalaryReport:
    db_salary_report = MonthlySalaryReport(**salary_report.dict(), generated_date=datetime.now())
    db.add(db_salary_report)
    db.commit()
    db.refresh(db_salary_report)
    return db_salary_report

def update_salary_report(db: Session, report_id: int, salary_report: MonthlySalaryReportUpdate) -> Optional[MonthlySalaryReport]:
    db_salary_report = db.query(MonthlySalaryReport).filter(MonthlySalaryReport.report_id == report_id).first()
    if db_salary_report:
        for key, value in salary_report.dict(exclude_unset=True).items():
            setattr(db_salary_report, key, value)
        db.commit()
        db.refresh(db_salary_report)
    return db_salary_report

def delete_salary_report(db: Session, report_id: int) -> bool:
    db_salary_report = db.query(MonthlySalaryReport).filter(MonthlySalaryReport.report_id == report_id).first()
    if db_salary_report:
        db.delete(db_salary_report)
        db.commit()
        return True
    return False
def get_salary_reports_by_month(db: Session, month_year: str) -> List[MonthlySalaryReport]:
    return db.query(MonthlySalaryReport).filter(MonthlySalaryReport.month_year == month_year).all()

def generate_monthly_salary_report(db: Session, month_year: str):
    db.query(MonthlySalaryReport).filter(MonthlySalaryReport.month_year == month_year).delete()
    db.commit()
        # Get all payments for the month
    payments = db.query(LimoPayment).filter(
        extract('year', LimoPayment.payment_date) == int(month_year.split('-')[0]),
        extract('month', LimoPayment.payment_date) == int(month_year.split('-')[1])
    ).all()
    
    # Group by captain_id and calculate totals
    captain_totals = {}
    for payment in payments:
        if payment.captain_id not in captain_totals:
            captain_totals[payment.captain_id] = {
                'total_driver_payment': 0,
                'total_driver_base_cost': 0,
                'total_driver_other_cost': 0,
                'tips': 0
            }
        captain_totals[payment.captain_id]['total_driver_payment'] += float(payment.total_driver_payment)
        captain_totals[payment.captain_id]['total_driver_base_cost'] += float(payment.total_driver_base_cost)
        captain_totals[payment.captain_id]['total_driver_other_cost'] += float(payment.total_driver_other_cost)
        captain_totals[payment.captain_id]['tips'] += float(payment.tips)
    
    # Create salary reports
    for captain_id, totals in captain_totals.items():
        # Get employee details
        employee = db.query(Employee).filter(Employee.captain_id == captain_id).first()
        if not employee:
            continue
            
        # Get deductions for the month
        deduction = db.query(Deduction).filter(
            Deduction.employee_id == employee.employee_id,
            extract('year', Deduction.monthstart_date) == int(month_year.split('-')[0]),
            extract('month', Deduction.monthstart_date) == int(month_year.split('-')[1])
        ).first()
        
        # Calculate salary
        gross_pay = totals['total_driver_payment']
        deductions_total = float(deduction.vendor_fee if deduction else 0) + \
                        float(deduction.traffic_fine if deduction else 0) + \
                        float(deduction.loan_fine if deduction else 0) + \
                        float(deduction.training_fee if deduction else 0)
        net_salary = gross_pay - deductions_total
        
        # Create salary report
        salary_report = MonthlySalaryReportCreate(
            careem_captain_id=captain_id,
            person_code=employee.person_code,
            card_no=employee.card_no,
            designation=employee.designation,
            doj=employee.doj,
            name=employee.name,
            total_working_hours=0,
            no_of_days=0,
            total_orders=0,
            actual_order_pay=totals['total_driver_base_cost'],
            total_excess_pay=totals['total_driver_other_cost'],
            gross_pay=gross_pay,
            total_cod=0,
            vendor_fee=deduction.vendor_fee if deduction else 0,
            traffic_fine=deduction.traffic_fine if deduction else 0,
            loan_fine=deduction.loan_fine if deduction else 0,
            training_fee=deduction.training_fee if deduction else 0,
            net_salary=net_salary,
            month_year=month_year,
            remarks=deduction.remarks if deduction else None
        )
        
        create_salary_report(db, salary_report)
    
    return len(captain_totals)