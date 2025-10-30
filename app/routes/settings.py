from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.settings import SystemSettings, AuditLog
from passlib.context import CryptContext
from app.schemas.settings import (
    SettingsUpdate, UserCreate, UserResponse, 
    AuditLogResponse, SettingsResponse
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/settings", tags=["settings"])

# System Settings Endpoints
@router.get("/", response_model=SettingsResponse)
async def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SystemSettings).first()
    if not settings:
        # Create default settings if none exist
        settings = SystemSettings(
            company_name="RiderApp Management",
            training_fee=500.00,
            cutoff_date=3,
            email_notifications=True,
            auto_generate_reports=True,
            currency="AED"
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/", response_model=SettingsResponse)
async def update_settings(settings_data: SettingsUpdate, db: Session = Depends(get_db)):
    settings = db.query(SystemSettings).first()
    if not settings:
        settings = SystemSettings(**settings_data.dict())
        db.add(settings)
    else:
        for key, value in settings_data.dict().items():
            setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings

# User Management Endpoints
@router.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Map frontend roles to backend roles
    role_mapping = {
        "Administrator": UserRole.admin,
        "Manager": UserRole.manager,
        "Staff": UserRole.user
    }
    
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=pwd_context.hash(user_data.password),
        role=role_mapping.get(user_data.role, UserRole.user),
        status="active"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Audit Log Endpoints
@router.get("/audit-log", response_model=List[AuditLogResponse])
async def get_audit_log(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()

# Role Permissions Endpoints
@router.get("/roles")
async def get_role_permissions():
    return {
        "Administrator": "Full access to all modules including system settings, user management, and data deletion",
        "Manager": "Can manage employees, partners, upload data, and generate reports. Cannot access system settings",
        "Staff": "Can view data and basic reports. Cannot modify employee records or upload data"
    }