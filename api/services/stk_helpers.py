from datetime import datetime
import base64
from api.core.config import setting

"""
    Providing reusable helper functions.
    Generate a timestamp in the format required by Safaricom Daraja API (YYYYMMDDHHMMSS).
"""
def generate_timestamp()->str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def generate_password(timestamp:str)->str:
    password=(
        setting.BUSINESS_SHORT_CODE +
        setting.PASSKEY +
        timestamp
    )
    return base64.b64encode(password.encode()).decode() 
    
    
 