# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/weekly-trips")
async def upload_weekly_trips(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")
    
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))
        
        # Process the Excel file and return summary
        total_records = len(df)
        # Add your data processing logic here
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "total_records": total_records,
            "valid_records": total_records,  # Adjust based on validation
            "errors": 0  # Adjust based on validation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")