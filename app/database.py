# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://riderapp_db_user:nyQiOuI8KGN3SljmvfFMHwIUGJjumwcm@dpg-d40q97ruibrs73cmdts0-a.singapore-postgres.render.com/riderapp_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
from app.models import employee, partner, wps_vendor, weekly_trip, deduction, monthly_salary_report, user