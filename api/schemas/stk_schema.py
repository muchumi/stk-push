from pydantic import BaseModel, Field

class STKPushRequest(BaseModel):
    phoneNumber: str = Field(..., example="+254719271870", description="Customer number in international format")
    amount: float = Field(..., gt=0, example=100.00, description="Amount to be charged")
    accountReference: str = Field(..., min_length=1, max_length=20, example="INV001", description="Reference for the transaction")
    transactionDescription: str = Field(..., min_length=1, max_length=50, example="Payment For Goods", description="Description of the transaction")
