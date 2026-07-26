import base64
import requests
from fastapi import HTTPException, status
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
    try:
        response=requests.get(
            settings.OAUTH_URL,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to connect to Safaricom Daraja API Service: {str(e)}")
    data=response.json()
    token=data.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="No access token returned from Safaricom Daraja API")
    return token




