from fastapi import APIRouter, Request, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.db.database import get_db
from typing import Optional
from api.models.stk_transaction import STKTransaction 
from api.schemas.STKPushRequest import STKPushRequest
from api.schemas.STKTransaction import STKTransactionResponse
from api.services.stk_push import initiate_stk_push
from api.services.stk_query import query_stk_status

router = APIRouter(prefix="/stk", tags=["STK Push"])

"""
    This is the STK Push API endpoint.It is used to initiate an STK Push to Safaricom Daraja API after receiving a payment request.
    It saves the transaction details in the database and returns the saved transaction details as a response to the client.
"""
@router.post("/push", response_model=STKTransactionResponse, status_code=status.HTTP_201_CREATED)
def stk_push(request: STKPushRequest, db: Session = Depends(get_db)):
    # Initiating the STK Push request to Safaricom Daraja API using the provided phone number and amount
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
    return transaction

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
            metadata=stk_callback["CallbackMetadata"]["Item"]
            data={}
            for item in metadata:
                data[item["Name"]]=item.get("Value")
            transaction.status="success"
            transaction.phoneNumber=data.get("PhoneNumber")
            transaction.mpesa_receipt_number=data.get("MpesaReceiptNumber")
            transaction.transaction_date=data.get("TransactionDate")    
        else:
            transaction.status="failed"
        db.commit()
        db.refresh(transaction)
    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted",
        "message": "Callback received and processed successfully."
    }            


"""
    This endpoint/route acts as a transaction status checker.
    It allows our application to ask Safaricom for the current status of a specific STK Push transaction.
"""
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


"""
    This endpoint/route gets all transactions from the database.
"""
@router.get("/transactions", response_model=list[STKTransactionResponse],status_code=status.HTTP_200_OK)
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(STKTransaction).all()
    return transactions


"""
    This endpoint/route enables searching for transactions.
"""
@router.get("/transactions/search", response_model=list[STKTransactionResponse], status_code=status.HTTP_200_OK)
def search_transactions(phoneNumber: Optional[str]=None, status: Optional[str]=None, checkout_request_id: Optional[str]=None, merchant_request_id: Optional[str]=None, mpesa_receipt_number: Optional[str]=None, db: Session = Depends(get_db)):
    query=db.query(STKTransaction)
    if phoneNumber:
        query=query.filter(STKTransaction.phoneNumber==phoneNumber)
    if status:
        query=query.filter(STKTransaction.status==status)
    if checkout_request_id:
        query=query.filter(STKTransaction.checkout_request_id==checkout_request_id)
    if merchant_request_id:
        query=query.filter(STKTransaction.merchant_request_id==merchant_request_id)
    if mpesa_receipt_number:
        query=query.filter(STKTransaction.mpesa_receipt_number==mpesa_receipt_number)

    return query.all() 


"""
    This endpoint/route gets a single transaction by id.
    It is used in retrieving single transaction results.
"""
@router.get("/transactions/{transaction_id}", response_model=STKTransactionResponse, status_code=status.HTTP_200_OK)
def get_single_transaction(transaction_id: int, db: Session = Depends(get_db)):
    single_transaction=db.query(STKTransaction).filter(STKTransaction.id==transaction_id).first()
    if not single_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction resource not found")
    return single_transaction


    
