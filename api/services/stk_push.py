from api.services.auth import get_access_token
from api.services.stk_helpers import generate_timestamp, generate_password

# Handles communication with Safaricom Daraja API for STK Push requests
def initiate_stk_push(phoneNumber: str, amount: int):
    token=get_access_token()
    timestamp=generate_timestamp()
    password=generate_password(timestamp)





