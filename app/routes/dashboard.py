from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta
from app.database import get_db
from app.models.employee import Employee
from app.models.weekly_trip import WeeklyTrip
from app.models.deduction import Deduction
from app.models.partner import Partner
from typing import List, Dict, Any

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    # Total active employees
    total_employees = db.query(Employee).filter(Employee.status == "Active").count()
    
    # Employees joined this month
    current_month = datetime.now().month
    current_year = datetime.now().year
    employees_this_month = db.query(Employee).filter(
        extract('month', Employee.doj) == current_month,
        extract('year', Employee.doj) == current_year
    ).count()
    
    # Get recent weekly trips for order stats
    recent_trips = db.query(WeeklyTrip).filter(
        WeeklyTrip.week_start_date >= datetime.now() - timedelta(days=30)
    ).all()
    
    total_orders = sum(trip.total_orders or 0 for trip in recent_trips)
    total_cod = sum(float(trip.cod_collected or 0) for trip in recent_trips)
    total_hours = sum(float(trip.total_working_hours or 0) for trip in recent_trips)
    
    # Calculate changes (you can enhance this with actual comparison logic)
    prev_month_trips = db.query(WeeklyTrip).filter(
        WeeklyTrip.week_start_date >= datetime.now() - timedelta(days=60),
        WeeklyTrip.week_start_date < datetime.now() - timedelta(days=30)
    ).all()
    
    prev_orders = sum(trip.total_orders or 0 for trip in prev_month_trips)
    prev_cod = sum(float(trip.cod_collected or 0) for trip in prev_month_trips)
    prev_hours = sum(float(trip.total_working_hours or 0) for trip in prev_month_trips)
    
    orders_change = "+0.0%"
    cod_change = "+0.0%"
    hours_change = "+0.0%"
    
    if prev_orders > 0:
        orders_pct = ((total_orders - prev_orders) / prev_orders) * 100
        orders_change = f"{'+' if orders_pct >= 0 else ''}{orders_pct:.1f}%"
    
    if prev_cod > 0:
        cod_pct = ((total_cod - prev_cod) / prev_cod) * 100
        cod_change = f"{'+' if cod_pct >= 0 else ''}{cod_pct:.1f}%"
    
    if prev_hours > 0:
        hours_pct = ((total_hours - prev_hours) / prev_hours) * 100
        hours_change = f"{'+' if hours_pct >= 0 else ''}{hours_pct:.1f}%"
    
    return {
        "total_orders": f"{total_orders:,}",
        "active_riders": total_employees,
        "employees_this_month": employees_this_month,
        "total_cod": f"AED {total_cod:,.0f}",
        "total_hours": f"{total_hours:,.0f}",
        "orders_change": orders_change,
        "riders_change": f"+{employees_this_month}",
        "cod_change": cod_change,
        "hours_change": hours_change
    }

@router.get("/partner-performance")
async def get_partner_performance(db: Session = Depends(get_db)):
    # Get partner performance from weekly trips (you'll need to add partner_id to WeeklyTrip model)
    partner_performance = db.query(
        Partner.partner_name,
        func.sum(WeeklyTrip.total_orders).label('orders'),
        func.sum(WeeklyTrip.cod_collected).label('cod'),
        func.sum(WeeklyTrip.total_working_hours).label('hours')
    ).join(Employee, Employee.employee_id == WeeklyTrip.employee_id)\
     .join(Partner, Partner.partner_id == Employee.partner_id)\
     .group_by(Partner.partner_name)\
     .filter(WeeklyTrip.week_start_date >= datetime.now() - timedelta(days=30))\
     .all()
    
    return [
        {
            "name": row.partner_name,
            "orders": int(row.orders or 0),
            "cod": float(row.cod or 0),
            "hours": float(row.hours or 0)
        }
        for row in partner_performance
    ]

@router.get("/order-distribution")
async def get_order_distribution(db: Session = Depends(get_db)):
    # Get order distribution by partner
    distribution = db.query(
        Partner.partner_name,
        func.sum(WeeklyTrip.total_orders).label('orders')
    ).join(Employee, Employee.employee_id == WeeklyTrip.employee_id)\
     .join(Partner, Partner.partner_id == Employee.partner_id)\
     .group_by(Partner.partner_name)\
     .filter(WeeklyTrip.week_start_date >= datetime.now() - timedelta(days=30))\
     .all()
    
    total_orders = sum(row.orders or 0 for row in distribution)
    
    colors = ["#10b981", "#3b82f6", "#f59e0b", "#8b5cf6", "#ef4444", "#06b6d4"]
    
    return [
        {
            "name": row.partner_name,
            "value": round(((row.orders or 0) / total_orders) * 100) if total_orders > 0 else 0,
            "color": colors[i % len(colors)]
        }
        for i, row in enumerate(distribution)
    ]

@router.get("/employee-joins")
async def get_employee_joins(db: Session = Depends(get_db)):
    # Get employee joins per month for the last 12 months
    twelve_months_ago = datetime.now() - timedelta(days=365)
    
    joins_by_month = db.query(
        func.to_char(Employee.doj, 'Mon YYYY').label('month'),
        func.count(Employee.employee_id).label('employees')
    ).filter(
        Employee.doj >= twelve_months_ago,
        Employee.doj.isnot(None)
    ).group_by('month').order_by('month').all()
    
    return [{"month": row.month, "employees": row.employees} for row in joins_by_month]

@router.get("/weekly-deductions")
async def get_weekly_deductions(db: Session = Depends(get_db)):
    # Get weekly deductions by partner for the last 8 weeks
    eight_weeks_ago = datetime.now() - timedelta(weeks=8)
    
    weekly_deductions_data = db.query(
        func.date_trunc('week', Deduction.monthstart_date).label('week'),
        Partner.partner_name,
        func.sum(Deduction.vendor_fee + Deduction.traffic_fine + Deduction.loan_fine + 
                Deduction.training_fee + Deduction.others).label('total_deductions')
    ).join(Employee, Employee.employee_id == Deduction.employee_id)\
     .join(Partner, Partner.partner_id == Employee.partner_id)\
     .filter(Deduction.monthstart_date >= eight_weeks_ago)\
     .group_by('week', Partner.partner_name)\
     .order_by('week')\
     .all()
    
    # Format the data for the chart
    result = {}
    for row in weekly_deductions_data:
        week_key = f"Week {row.week.isocalendar()[1]}"
        if week_key not in result:
            result[week_key] = {"week": week_key}
        result[week_key][row.partner_name] = float(row.total_deductions or 0)
    
    return list(result.values())

@router.get("/top-performers")
async def get_top_performers(db: Session = Depends(get_db)):
    # Get top performers based on orders in the last 30 days
    top_performers = db.query(
        Employee.name,
        func.sum(WeeklyTrip.total_orders).label('total_orders'),
        func.sum(WeeklyTrip.actual_order_pay + WeeklyTrip.excess_pay).label('total_earnings'),
        Partner.partner_name
    ).join(WeeklyTrip, WeeklyTrip.employee_id == Employee.employee_id)\
     .join(Partner, Partner.partner_id == Employee.partner_id)\
     .filter(WeeklyTrip.week_start_date >= datetime.now() - timedelta(days=30))\
     .group_by(Employee.employee_id, Employee.name, Partner.partner_name)\
     .order_by(func.sum(WeeklyTrip.total_orders).desc())\
     .limit(5)\
     .all()
    
    return [
        {
            "name": row.name,
            "orders": int(row.total_orders or 0),
            "earnings": f"AED {float(row.total_earnings or 0):,.0f}",
            "partner": row.partner_name
        }
        for row in top_performers
    ]

@router.get("/alerts")
async def get_dashboard_alerts(db: Session = Depends(get_db)):
    alerts = []
    
    # Check for unlinked WPS vendors
    unlinked_count = db.query(Employee).filter(Employee.wps_vendor_id.is_(None)).count()
    if unlinked_count > 0:
        alerts.append({
            "type": "info", 
            "message": f"{unlinked_count} riders not linked to WPS vendor"
        })
    
    # Check for recent weekly uploads (you might want to add an upload tracking system)
    recent_upload = db.query(WeeklyTrip).order_by(WeeklyTrip.week_start_date.desc()).first()
    if recent_upload:
        days_since_upload = (datetime.now().date() - recent_upload.week_start_date).days
        if days_since_upload > 7:
            alerts.append({
                "type": "warning", 
                "message": f"Weekly upload is {days_since_upload} days overdue"
            })
    
    return alerts