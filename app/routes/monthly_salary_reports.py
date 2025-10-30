from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.monthly_salary_report import MonthlySalaryReport, MonthlySalaryReportCreate, MonthlySalaryReportUpdate
from app.crud import monthly_salary_report as crud
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
import io
import pandas as pd
import datetime

router = APIRouter(prefix="/monthly-salary-reports", tags=["monthly-salary-reports"])

@router.post("/", response_model=MonthlySalaryReport)
def create_salary_report(salary_report: MonthlySalaryReportCreate, db: Session = Depends(get_db)):
    return crud.create_salary_report(db=db, salary_report=salary_report)

@router.get("/", response_model=list[MonthlySalaryReport])
def read_salary_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    salary_reports = crud.get_salary_reports(db, skip=skip, limit=limit)
    return salary_reports

@router.get("/month/{month_year}", response_model=list[MonthlySalaryReport])
def read_salary_reports_by_month(month_year: str, db: Session = Depends(get_db)):
    salary_reports = crud.get_salary_reports_by_month(db, month_year=month_year)
    return salary_reports

@router.get("/export-pdf")
def export_salary_pdf(month_year: str, db: Session = Depends(get_db)):
    try:
        salary_reports = crud.get_salary_reports_by_month(db, month_year=month_year)
        if not salary_reports:
            raise HTTPException(status_code=404, detail="No salary reports found for this month")
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        
        # PDF Header
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, f"Monthly Salary Report - {month_year}")
        p.setFont("Helvetica", 10)
        p.drawString(100, 780, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        p.drawString(100, 765, f"Total Employees: {len(salary_reports)}")
        
        # Table Headers
        y = 740
        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "Name")
        p.drawString(200, y, "Captain ID")
        p.drawString(300, y, "Gross Pay")
        p.drawString(400, y, "Deductions")
        p.drawString(500, y, "Net Salary")
        
        # Table Data
        y = 720
        p.setFont("Helvetica", 9)
        for report in salary_reports:
            deductions = (report.vendor_fee or 0) + (report.traffic_fine or 0) + (report.loan_fine or 0) + (report.training_fee or 0)
            p.drawString(50, y, report.name or "N/A")
            p.drawString(200, y, report.careem_captain_id or "N/A")
            p.drawString(300, y, f"{report.gross_pay:.2f}")
            p.drawString(400, y, f"{deductions:.2f}")
            p.drawString(500, y, f"{report.net_salary:.2f}")
            y -= 15
            if y < 50:  # New page if running out of space
                p.showPage()
                y = 800
        
        p.save()
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="application/pdf", 
                               headers={"Content-Disposition": f"attachment; filename=salary_report_{month_year}.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")

@router.get("/export-excel")
def export_salary_excel(month_year: str, db: Session = Depends(get_db)):
    try:
        salary_reports = crud.get_salary_reports_by_month(db, month_year=month_year)
        if not salary_reports:
            raise HTTPException(status_code=404, detail="No salary reports found for this month")
        
        # Convert to DataFrame with all relevant fields
        data = []
        for report in salary_reports:
            data.append({
                'Name': report.name,
                'Captain ID': report.careem_captain_id,
                'Person Code': report.person_code,
                'Designation': report.designation,
                'Total Working Hours': report.total_working_hours,
                'Total Orders': report.total_orders,
                'Actual Order Pay': report.actual_order_pay,
                'Total Excess Pay': report.total_excess_pay,
                'Gross Pay': report.gross_pay,
                'Vendor Fee': report.vendor_fee,
                'Traffic Fine': report.traffic_fine,
                'Loan Fine': report.loan_fine,
                'Training Fee': report.training_fee,
                'Total Deductions': (report.vendor_fee or 0) + (report.traffic_fine or 0) + (report.loan_fine or 0) + (report.training_fee or 0),
                'Net Salary': report.net_salary,
                'Remarks': report.remarks
            })
        
        df = pd.DataFrame(data)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'Salary Report {month_year}', index=False)
        
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               headers={"Content-Disposition": f"attachment; filename=salary_report_{month_year}.xlsx"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel export failed: {str(e)}")

@router.post("/generate/{month_year}")
def generate_monthly_report(month_year: str, db: Session = Depends(get_db)):
    try:
        reports_count = crud.generate_monthly_salary_report(db, month_year)
        return {"message": f"Monthly report generated for {month_year}", "reports_created": reports_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/{report_id}", response_model=MonthlySalaryReport)
def read_salary_report(report_id: int, db: Session = Depends(get_db)):
    db_salary_report = crud.get_salary_report(db, report_id=report_id)
    if db_salary_report is None:
        raise HTTPException(status_code=404, detail="Salary report not found")
    return db_salary_report

@router.put("/{report_id}", response_model=MonthlySalaryReport)
def update_salary_report(report_id: int, salary_report: MonthlySalaryReportUpdate, db: Session = Depends(get_db)):
    db_salary_report = crud.update_salary_report(db, report_id=report_id, salary_report=salary_report)
    if db_salary_report is None:
        raise HTTPException(status_code=404, detail="Salary report not found")
    return db_salary_report

@router.delete("/{report_id}")
def delete_salary_report(report_id: int, db: Session = Depends(get_db)):
    success = crud.delete_salary_report(db, report_id=report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Salary report not found")
    return {"message": "Salary report deleted successfully"}