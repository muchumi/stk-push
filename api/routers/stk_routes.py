from fastapi import APIRouter

router = APIRouter(prefix="/stk", tags=["STK Push"])

@router.post("/push")
def stk_push():
    return {"message": "STK push initiated"}