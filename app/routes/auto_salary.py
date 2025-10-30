# app/routes/auto_salary.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.salary_calculator import calculate_monthly_salary
from app.crud import monthly_salary_report as salary_report_crud
from app.schemas.monthly_salary_report import MonthlySalaryReportCreate

router = APIRouter(prefix="/auto-salary", tags=["auto-salary"])

@router.post("/generate/{employee_id}/{month_year}")
def generate_salary_report(employee_id: int, month_year: str, db: Session = Depends(get_db)):
    try:
        # Calculate salary
        salary_data = calculate_monthly_salary(db, employee_id, month_year)
        
        if "error" in salary_data:
            raise HTTPException(status_code=404, detail=salary_data["error"])
        
        # Create salary report
        salary_report = MonthlySalaryReportCreate(**salary_data)
        result = salary_report_crud.create_salary_report(db, salary_report)
        
        return {
            "message": "Salary report generated successfully",
            "report_id": result.report_id,
            "net_salary": result.net_salary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating salary: {str(e)}")

@router.post("/generate-all/{month_year}")
def generate_all_salaries(month_year: str, db: Session = Depends(get_db)):
    try:
        # This would need employee CRUD to get all employees
        # For now, return instruction
        return {
            "message": "Use /generate/{employee_id}/{month_year} for individual employees",
            "note": "Implement get_all_employees in CRUD to use this endpoint"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating salaries: {str(e)}")