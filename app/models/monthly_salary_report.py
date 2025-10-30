from sqlalchemy import Column, String, Integer, DECIMAL, TIMESTAMP, TEXT
from app.database import Base

class MonthlySalaryReport(Base):
    __tablename__ = "monthly_salary_reports"

    report_id = Column(Integer, primary_key=True, index=True)
    careem_captain_id = Column(String(20))
    person_code = Column(String(20))
    card_no = Column(String(30))
    designation = Column(String(50))
    doj = Column(String(20))
    name = Column(String(100))
    total_working_hours = Column(DECIMAL(10, 2))
    no_of_days = Column(Integer)
    total_orders = Column(Integer)
    actual_order_pay = Column(DECIMAL(10, 2))
    total_excess_pay = Column(DECIMAL(10, 2))
    gross_pay = Column(DECIMAL(10, 2))
    total_cod = Column(DECIMAL(10, 2))
    vendor_fee = Column(DECIMAL(10, 2))
    traffic_fine = Column(DECIMAL(10, 2))
    loan_fine = Column(DECIMAL(10, 2))
    training_fee = Column(DECIMAL(10, 2))
    net_salary = Column(DECIMAL(10, 2))
    remarks = Column(TEXT)
    month_year = Column(String(10))
    generated_date = Column(TIMESTAMP)