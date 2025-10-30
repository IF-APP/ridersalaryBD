from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.limo_payment import LimoPayment, LimoPaymentCreate, LimoPaymentUpdate
from app.crud import limo_payment as crud
from datetime import datetime
import pandas as pd
import io
from app.models.limo_payment import LimoPayment as LimoPaymentModel


router = APIRouter(prefix="/limo-payments", tags=["limo-payments"])

@router.post("/", response_model=LimoPayment)
def create_limo_payment(payment: LimoPaymentCreate, db: Session = Depends(get_db)):
    return crud.create_limo_payment(db=db, payment=payment)

@router.get("/", response_model=list[LimoPayment])
def read_limo_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_limo_payments(db, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=LimoPayment)
def read_limo_payment(payment_id: str, db: Session = Depends(get_db)):
    db_payment = crud.get_limo_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/{payment_id}", response_model=LimoPayment)
def update_limo_payment(payment_id: str, payment: LimoPaymentUpdate, db: Session = Depends(get_db)):
    db_payment = crud.update_limo_payment(db, payment_id=payment_id, payment=payment)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.delete("/{payment_id}")
def delete_limo_payment(payment_id: str, db: Session = Depends(get_db)):
    success = crud.delete_limo_payment(db, payment_id=payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}
# @router.post("/upload/")
# async def upload_limo_payments(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         if not file.filename.endswith(('.xlsx', '.xls')):
#             raise HTTPException(status_code=400, detail="Only Excel files allowed")
        
#         # Read and process the Excel file
#         contents = await file.read()
#         df = pd.read_excel(io.BytesIO(contents))
        
#         # Process each row and save to database
#         processed_count = 0
#         for index, row in df.iterrows():
#             payment_data = LimoPaymentCreate(
#     limo_company=str(row['limo_company']),
#     limo_company_id=str(row['limo_company_id']),  # Convert to string
#     captain_name=str(row['captain_name']),
#     captain_id=str(row['captain_id']),  # Convert to string
#     payment_date=row['payment_date'],
#     payment_id=str(row['payment_id']),  # Convert to string
#     payment_method=str(row['payment_method']),
#     total_driver_base_cost=float(row['total_driver_base_cost']),
#     total_driver_other_cost=float(row['total_driver_other_cost']),
#     total_driver_payment=float(row['total_driver_payment']),
#     tips=float(row.get('tips', 0))
# )
#             crud.create_limo_payment(db, payment_data)
#             processed_count += 1
        
#         return {
#             "message": "File uploaded and processed successfully",
#             "filename": file.filename,
#             "processed_records": processed_count
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
@router.post("/upload/")
async def upload_limo_payments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files allowed")
        
        # Check if filename already exists
        existing_file = db.query(LimoPaymentModel).filter(LimoPaymentModel.filename == file.filename).first()
        if existing_file:
            raise HTTPException(status_code=400, detail="File already exists")
        
        # Read and process the Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Process each row and save to database
        processed_count = 0
        for index, row in df.iterrows():
            payment_data = LimoPaymentCreate(
                limo_company=str(row['limo_company']),
                limo_company_id=str(row['limo_company_id']),
                captain_name=str(row['captain_name']),
                captain_id=str(row['captain_id']),
                payment_date=row['payment_date'],
                payment_id=str(row['payment_id']),
                payment_method=str(row['payment_method']),
                total_driver_base_cost=float(row['total_driver_base_cost']),
                total_driver_other_cost=float(row['total_driver_other_cost']),
                total_driver_payment=float(row['total_driver_payment']),
                tips=float(row.get('tips', 0)),
                filename=file.filename  # Add filename to each record
            )
            crud.create_limo_payment(db, payment_data)
            processed_count += 1
        
        return {
            "message": "File uploaded and processed successfully",
            "filename": file.filename,
            "processed_records": processed_count
        }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
