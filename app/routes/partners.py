# app/routes/partners.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.partner import Partner, PartnerCreate, PartnerUpdate
from app.crud import partner as crud

router = APIRouter(prefix="/partners", tags=["partners"])

@router.post("/", response_model=Partner)
def create_partner(partner: PartnerCreate, db: Session = Depends(get_db)):
    return crud.create_partner(db=db, partner=partner)

@router.get("/", response_model=list[Partner])
def read_partners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    partners = crud.get_partners(db, skip=skip, limit=limit)
    return partners

@router.get("/{partner_id}", response_model=Partner)
def read_partner(partner_id: int, db: Session = Depends(get_db)):
    db_partner = crud.get_partner(db, partner_id=partner_id)
    if db_partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")
    return db_partner

@router.put("/{partner_id}", response_model=Partner)
def update_partner(partner_id: int, partner: PartnerUpdate, db: Session = Depends(get_db)):
    db_partner = crud.update_partner(db, partner_id=partner_id, partner=partner)
    if db_partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")
    return db_partner

@router.delete("/{partner_id}")
def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    success = crud.delete_partner(db, partner_id=partner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"message": "Partner deleted successfully"}