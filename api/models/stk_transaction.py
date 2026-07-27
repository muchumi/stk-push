from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from api.db.database import Base

class STKTransaction(Base):
    __tablename__ = "stk_transactions"

    id = Column(Integer, primary_key=True, index=True)
    merchant_request_id = Column(String, nullable=True)
    checkout_request_id = Column(String, unique=True, nullable=True)
    phoneNumber = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="Pending")
    mpesa_receipt_number = Column(String, nullable=True)
    result_code = Column(Integer, nullable=True)
    result_desc = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())