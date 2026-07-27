import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    BUSINESS_SHORT_CODE = os.getenv("BUSINESS_SHORT_CODE")
    PASSKEY = os.getenv("PASSKEY")
    OAUTH_URL = os.getenv("OAUTH_URL")
    STK_PUSH_URL = os.getenv("STK_PUSH_URL")
    CALLBACK_URL = os.getenv("CALLBACK_URL")
    BASE_URL="https://sandbox.safaricom.co.ke"

setting=Settings()