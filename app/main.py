from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user import User, UserRole 
from app.routes import settings
from app.database import create_tables, get_db
from app.routes import (
    dashboard,
    employees, 
    partners, 
    wps_vendors, 
    weekly_trips, 
    deductions, 
    monthly_salary_reports,
    auto_salary,
    limo_payments
)

# Global variables
blacklisted_tokens = set()
SECRET_KEY = "your-secret-key-here-must-be-32-chars"
JWT_REFRESH_SECRET_KEY = "your-refresh-secret-key-32-chars"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Auth router and functions
router = APIRouter(prefix="/auth", tags=["authentication"])

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}, 
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "role": user.role.value}
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "email": user.email,
        "role": user.role.value
    }

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    blacklisted_tokens.add(token)
    return {"message": "Logged out successfully"}

@router.post("/refresh")
async def refresh_token(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    if refresh_token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")
        
        new_access_token = create_access_token(
            data={"sub": user.email, "role": user.role.value},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "role": user.role.value
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/reset-password")
async def reset_password(
    token: str = Body(..., embed=True), 
    new_password: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        user.hashed_password = pwd_context.hash(new_password)
        db.commit()
        return {"message": "Password reset successful"}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/generate-reset-token")
async def generate_reset_token(
    email: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=15)
    )
    return {"reset_token": reset_token}

def create_default_users():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        if not db.query(User).first():
            admin = User(
                email="admin@riderapp.com",
                hashed_password=pwd_context.hash("admin123"),
                role=UserRole.admin,
                name="Admin User"
            )
            user = User(
                email="ahmed@riderapp.com", 
                hashed_password=pwd_context.hash("user123"),
                role=UserRole.user,
                name="Ahmed Hassan"
            )
            db.add(admin)
            db.add(user)
            db.commit()
    finally:
        db.close()

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router)
app.include_router(employees.router)
app.include_router(partners.router)
app.include_router(wps_vendors.router)
app.include_router(weekly_trips.router)
app.include_router(deductions.router)
app.include_router(monthly_salary_reports.router)
app.include_router(auto_salary.router)
app.include_router(limo_payments.router)
app.include_router(settings.router)
app.include_router(router)

@app.on_event("startup")
def on_startup():
    create_tables()
    create_default_users()

@app.get("/")
def read_root():
    return {"message": "Rider Salary Management System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)