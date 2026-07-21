from fastapi import APIRouter

routes = APIRouter(prefix="/stk", tags=["STK Push"])

@routes.post("/push")
def stk_push():
    return {"message": "STK push initiated"}