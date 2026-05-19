import requests

from config import API_URL, VERIFY_SSL
from services.session import get_token
from services.api_client import api_get, api_post


def login(email, password):
    url = f"{API_URL}/api/authentication/login"

    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, json=data, verify=VERIFY_SSL)

    if response.status_code == 200:
        return response.json().get("token")

    return None


def get_user_profile():
    response = api_get("/api/authentication/me")
    return response.json()


def logout():
    api_post("/api/authentication/logout")


def register(email, username, password):
    data = {
        "email": email,
        "username": username,
        "password": password
    }

    response = api_post("/api/authentication/register", data)

    if response.status_code == 200:
        return True, None

    try:
        error_data = response.json()
        return False, error_data.get("detail", "Registration failed.")
    except Exception:
        return False, "Registration failed."


def forgot_password(email):
    data = {
        "email": email
    }

    response = api_post("/api/authentication/forgot-password", data)

    return response.status_code == 200