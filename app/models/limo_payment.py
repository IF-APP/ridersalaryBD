from sqlalchemy import Column, String, Integer, Date, DECIMAL, TIMESTAMP
from app.database import Base
from datetime import datetime

class LimoPayment(Base):
    __tablename__ = "limo_payments"

    payment_id = Column(String(100), primary_key=True, index=True)  # Change this line
    limo_company = Column(String(255), nullable=False)
    limo_company_id = Column(String(100), nullable=False)
    captain_name = Column(String(255), nullable=False)
    captain_id = Column(String(100), nullable=False)
    payment_date = Column(Date, nullable=False)
    # Remove the duplicate payment_id line below
    payment_method = Column(String(50), nullable=False)
    total_driver_base_cost = Column(DECIMAL(10,2), nullable=False)
    total_driver_other_cost = Column(DECIMAL(10,2), default=0.00)
    total_driver_payment = Column(DECIMAL(10,2), nullable=False)
    tips = Column(DECIMAL(10,2), default=0.00)
    created_at = Column(TIMESTAMP, default=datetime.now)
    filename = Column(String(255))  # Add this line
