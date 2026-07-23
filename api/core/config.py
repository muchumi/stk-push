import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

SHORTCODE = os.getenv("SHORTCODE")
PASSKEY = os.getenv("PASSKEY")

CALLBACK_URL = os.getenv("CALLBACK_URL")

BASE_URL="https://sandbox.safaricom.co.ke"