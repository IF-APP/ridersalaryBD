# app/models/weekly_trip.py
from sqlalchemy import Column, String, Integer, Date, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import weekly_trip
class WeeklyTrip(Base):
    __tablename__ = "weekly_trips"

    trip_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    week_start_date = Column(Date, nullable=False)
    week_end_date = Column(Date, nullable=False)
    total_working_hours = Column(DECIMAL(10, 2))
    total_orders = Column(Integer)
    actual_order_pay = Column(DECIMAL(10, 2))
    excess_pay = Column(DECIMAL(10, 2))
    cod_collected = Column(DECIMAL(10, 2))
    upload_batch_id = Column(Integer)
    created_at = Column(TIMESTAMP)

    employee = relationship("Employee", back_populates="weekly_trips")