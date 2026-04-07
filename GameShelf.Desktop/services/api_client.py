import requests
from config import API_URL
from services.session import get_token

def get_me():
    url = f"{API_URL}/api/authentication/me"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, verify=False)

    return response