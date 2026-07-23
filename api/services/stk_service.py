import base64
import requests

from api.core.config import settings

def get_access_token():
    """
        Generate an OAuth access token from Sfaricom Daraja API.
    """
    # Combining consumer key consumer secret to create a base64 encoded string
    credentials=f"{settings.CONSUMER_KEY}:{settings.CONSUMER_SECRET}"
    # Encode the credentials to base64
    encoded_credentials=base64.b64encode(credentials.encode()).decode()

    headers={
        "Authorization": f"Basic {encoded_credentials}"
    }

    response=requests.get(
        settings.OAUTH_URL,
        headers=headers
    )
    response.raise_for_status()
    token=response.json()["access_token"]
    return token




