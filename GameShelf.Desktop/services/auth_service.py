import requests
from config import API_URL
from services.session import get_token

def login(email, password):
    url = f"{API_URL}/api/authentication/login"

    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, json=data, verify=False)

    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None

def get_user_profile():
    url = f"{API_URL}/api/authentication/me"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, verify=False)

    return response.json()

def logout():
    url = f"{API_URL}/api/authentication/logout"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    requests.post(url, headers=headers, verify=False)