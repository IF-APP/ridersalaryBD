# app/routes/employees.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from app.crud import employee as crud

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

@router.get("/", response_model=list[Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@router.get("/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    success = crud.delete_employee(db, employee_id=employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}