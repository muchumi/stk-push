from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.models.stk_transaction import STKTransaction 
from api.schemas.STKPushRequest import STKPushRequest
from api.services.stk_push import initiate_stk_push
from api.services.stk_query import query_stk_status

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
async def stk_callback(request: Request, db: Session = Depends(get_db)):
    callback_data=await request.json()
    stk_callback=callback_data["Body"]["stkCallback"]
    checkout_request_id=stk_callback["CheckoutRequestID"]
    result_code=stk_callback["ResultCode"]
    result_desc=stk_callback["ResultDesc"]

    transaction=(db.query(STKTransaction).filter(STKTransaction.checkout_request_id==checkout_request_id).first())
    if transaction:
        if result_code==0:
            transaction.status="success"
        else:
            transaction.status="failed"
    db.commit()
    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted",
        "message": "Callback received and processed successfully."
    }            


@router.get("/status/{checkout_request_id}")
def stk_status(
    checkout_request_id: str,
    db: Session = Depends(get_db)
):
    response = query_stk_status(checkout_request_id)

    transaction = (
        db.query(STKTransaction)
        .filter(
            STKTransaction.checkout_request_id == checkout_request_id
        )
        .first()
    )

    if transaction:

        result_code = response.get("ResultCode")
        result_desc = response.get("ResultDesc")

        transaction.result_desc = result_desc

        if result_code == "0" or result_code == 0:
            transaction.status = "success"
        else:
            transaction.status = "failed"

        db.commit()
        db.refresh(transaction)

    return response