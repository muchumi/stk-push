import base64
import requests
from datetime import datetime
from fastapi import HTTPException, status
from api.core.config import setting
from api.services.auth import get_access_token

def query_stk_status(checkout_request_id: str):
    access_token=get_access_token()
    timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
    password=base64.b64encode(f"{setting.SHORTCODE}{setting.PASSKEY}{timestamp}".encode()).decode()

    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload={
        "BusinessShortCode": setting.BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id
    }

    response=requests.post(
        setting.STK_QUERY_URL, 
        json=payload, 
        headers=headers
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.text
        )
    return response.json()
