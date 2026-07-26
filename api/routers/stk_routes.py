from fastapi import APIRouter, Request
from api.schemas.stk_schema import STKPushRequest
from api.services.stk_helpers import generate_timestamp, generate_password

router = APIRouter(prefix="/stk", tags=["STK Push"])

@router.post("/push")
def stk_push(request: STKPushRequest):
    return {
        "message": "STK push initiated",
        "data":request.model_dump()
    }

