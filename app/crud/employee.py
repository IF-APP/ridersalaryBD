# app/crud/employee.py
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from typing import List, Optional

def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate) -> Optional[Employee]:
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee:
        for key, value in employee.dict(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int) -> bool:
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return True
    return False