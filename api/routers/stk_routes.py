from fastapi import APIRouter, Request
from api.schemas.stk_schema import STKPushRequest
from api.services.stk_helpers import generate_timestamp, generate_password
from api.services.stk_push import initiate_stk_push

router = APIRouter(prefix="/stk", tags=["STK Push"])

@router.post("/push")
def stk_push(request: STKPushRequest):
    return initiate_stk_push(
        phone_number=request.phone_number,
        amount=request.amount
    )

