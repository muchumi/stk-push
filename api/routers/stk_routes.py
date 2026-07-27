from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.models.stk_transaction import STKTransaction 
from api.schemas.STKPushRequest import STKPushRequest
from api.services.stk_push import initiate_stk_push

router = APIRouter(prefix="/stk", tags=["STK Push"])

@router.post("/push")
def stk_push(request: STKPushRequest, db: Session = Depends(get_db)):
    response= initiate_stk_push(
        phoneNumber=request.phoneNumber,
        amount=request.amount
    )
    transaction=STKTransaction(
        phoneNumber=request.phoneNumber,
        amount=request.amount,
        merchant_request_id=response.get("MerchantRequestID"),
        checkout_request_id=response.get("CheckoutRequestID"),
        status="pending"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return response

"""
    Endpoint to handle the callback from Safaricom Daraja API after an STK Push request is initiated.
"""
@router.post("/callback")
async def stk_callback(request: Request):
    callback_data=await request.json()
    print(callback_data)
    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted" 
    }


