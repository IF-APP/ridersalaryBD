import enum
from sqlalchemy import Column, String, Integer, Enum
from app.database import Base

class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager" 
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    name = Column(String(100))
    status = Column(String(20), default="active")