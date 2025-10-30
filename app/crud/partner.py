# app/crud/partner.py
from sqlalchemy.orm import Session
from app.models.partner import Partner
from app.schemas.partner import PartnerCreate, PartnerUpdate
from typing import List, Optional

def get_partner(db: Session, partner_id: int) -> Optional[Partner]:
    return db.query(Partner).filter(Partner.partner_id == partner_id).first()

def get_partners(db: Session, skip: int = 0, limit: int = 100) -> List[Partner]:
    return db.query(Partner).offset(skip).limit(limit).all()

def create_partner(db: Session, partner: PartnerCreate) -> Partner:
    db_partner = Partner(**partner.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

def update_partner(db: Session, partner_id: int, partner: PartnerUpdate) -> Optional[Partner]:
    db_partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
    if db_partner:
        for key, value in partner.dict(exclude_unset=True).items():
            setattr(db_partner, key, value)
        db.commit()
        db.refresh(db_partner)
    return db_partner

def delete_partner(db: Session, partner_id: int) -> bool:
    db_partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
    if db_partner:
        db.delete(db_partner)
        db.commit()
        return True
    return False