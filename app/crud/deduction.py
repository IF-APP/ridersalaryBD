# app/crud/deduction.py
from sqlalchemy.orm import Session
from app.models.deduction import Deduction
from app.schemas.deduction import DeductionCreate, DeductionUpdate
from typing import List, Optional

def get_deduction(db: Session, deduction_id: int) -> Optional[Deduction]:
    return db.query(Deduction).filter(Deduction.deduction_id == deduction_id).first()

def get_deductions(db: Session, skip: int = 0, limit: int = 100) -> List[Deduction]:
    return db.query(Deduction).offset(skip).limit(limit).all()

def get_deductions_by_employee(db: Session, employee_id: int) -> List[Deduction]:
    return db.query(Deduction).filter(Deduction.employee_id == employee_id).all()

def create_deduction(db: Session, deduction: DeductionCreate) -> Deduction:
    db_deduction = Deduction(**deduction.dict())
    db.add(db_deduction)
    db.commit()
    db.refresh(db_deduction)
    return db_deduction

def update_deduction(db: Session, deduction_id: int, deduction: DeductionUpdate) -> Optional[Deduction]:
    db_deduction = db.query(Deduction).filter(Deduction.deduction_id == deduction_id).first()
    if db_deduction:
        for key, value in deduction.dict(exclude_unset=True).items():
            setattr(db_deduction, key, value)
        db.commit()
        db.refresh(db_deduction)
    return db_deduction

def delete_deduction(db: Session, deduction_id: int) -> bool:
    db_deduction = db.query(Deduction).filter(Deduction.deduction_id == deduction_id).first()
    if db_deduction:
        db.delete(db_deduction)
        db.commit()
        return True
    return False