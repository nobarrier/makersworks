import requests
import base64
from django.conf import settings

CLIENT_ID = settings.DIGIKEY_CLIENT_ID
CLIENT_SECRET = settings.DIGIKEY_CLIENT_SECRET
ENV = settings.DIGIKEY_ENV.lower()

if ENV == "sandbox":
    TOKEN_URL = "https://sandbox-api.digikey.com/v1/oauth2/token"
else:
    TOKEN_URL = "https://api.digikey.com/v1/oauth2/token"


def get_access_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("DIGIKEY_CLIENT_ID / DIGIKEY_CLIENT_SECRET missing")

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(TOKEN_URL, headers=headers, data=data, timeout=20)

    if response.status_code != 200:
        raise RuntimeError(
            f"DigiKey token request failed ({response.status_code}): {response.text}"
        )

    return response.json()["access_token"]
