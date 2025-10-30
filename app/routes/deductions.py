# app/routes/deductions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.deduction import Deduction, DeductionCreate, DeductionUpdate
from app.crud import deduction as crud

router = APIRouter(prefix="/deductions", tags=["deductions"])

@router.post("/", response_model=Deduction)
def create_deduction(deduction: DeductionCreate, db: Session = Depends(get_db)):
    return crud.create_deduction(db=db, deduction=deduction)

@router.get("/", response_model=list[Deduction])
def read_deductions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deductions = crud.get_deductions(db, skip=skip, limit=limit)
    return deductions

@router.get("/employee/{employee_id}", response_model=list[Deduction])
def read_deductions_by_employee(employee_id: int, db: Session = Depends(get_db)):
    deductions = crud.get_deductions_by_employee(db, employee_id=employee_id)
    return deductions

@router.get("/{deduction_id}", response_model=Deduction)
def read_deduction(deduction_id: int, db: Session = Depends(get_db)):
    db_deduction = crud.get_deduction(db, deduction_id=deduction_id)
    if db_deduction is None:
        raise HTTPException(status_code=404, detail="Deduction not found")
    return db_deduction

@router.put("/{deduction_id}", response_model=Deduction)
def update_deduction(deduction_id: int, deduction: DeductionUpdate, db: Session = Depends(get_db)):
    db_deduction = crud.update_deduction(db, deduction_id=deduction_id, deduction=deduction)
    if db_deduction is None:
        raise HTTPException(status_code=404, detail="Deduction not found")
    return db_deduction

@router.delete("/{deduction_id}")
def delete_deduction(deduction_id: int, db: Session = Depends(get_db)):
    success = crud.delete_deduction(db, deduction_id=deduction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Deduction not found")
    return {"message": "Deduction deleted successfully"}