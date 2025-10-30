from sqlalchemy.orm import Session
from app.models.limo_payment import LimoPayment
from app.schemas.limo_payment import LimoPaymentCreate, LimoPaymentUpdate
from typing import List, Optional
from datetime import datetime

def get_limo_payment(db: Session, payment_id: str) -> Optional[LimoPayment]:
    return db.query(LimoPayment).filter(LimoPayment.payment_id == payment_id).first()

def get_limo_payments(db: Session, skip: int = 0, limit: int = 100) -> List[LimoPayment]:
    return db.query(LimoPayment).offset(skip).limit(limit).all()

def create_limo_payment(db: Session, payment: LimoPaymentCreate) -> LimoPayment:
    db_payment = LimoPayment(**payment.dict(), created_at=datetime.now())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_limo_payment(db: Session, payment_id: str, payment: LimoPaymentUpdate) -> Optional[LimoPayment]:
    db_payment = db.query(LimoPayment).filter(LimoPayment.payment_id == payment_id).first()
    if db_payment:
        for key, value in payment.dict(exclude_unset=True).items():
            setattr(db_payment, key, value)
        db.commit()
        db.refresh(db_payment)
    return db_payment

def delete_limo_payment(db: Session, payment_id: str) -> bool:
    db_payment = db.query(LimoPayment).filter(LimoPayment.payment_id == payment_id).first()
    if db_payment:
        db.delete(db_payment)
        db.commit()
        return True
    return False