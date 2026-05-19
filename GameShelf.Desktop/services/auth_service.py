import requests

from config import API_URL, VERIFY_SSL
from services.api_client import api_get, api_post


def login(email, password):
    url = f"{API_URL}/api/authentication/login"

    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(
            url,
            json=data,
            verify=VERIFY_SSL,
            timeout=10
        )
    except requests.RequestException:
        return None

    if response.status_code == 200:
        return response.json().get("token")

    return None


def get_user_profile():
    response = api_get("/api/authentication/me")

    if response is None or response.status_code != 200:
        return {}

    return response.json()


def logout():
    api_post("/api/authentication/logout")


def register(email, username, password):
    data = {
        "email": email,
        "username": username,
        "password": password
    }

    response = api_post(
        "/api/authentication/register",
        data,
        auth_required=False
    )

    if response is None:
        return False, "Nie udało się połączyć z API."

    if response.status_code == 200:
        return True, None

    try:
        error_data = response.json()
        return False, error_data.get("detail", "Rejestracja nie powiodła się.")
    except Exception:
        return False, "Rejestracja nie powiodła się."


def forgot_password(email):
    data = {
        "email": email
    }

    response = api_post(
        "/api/authentication/forgot-password",
        data,
        auth_required=False
    )

    if response is None:
        return False

    return response.status_code == 200


def reset_password(email, token, new_password):
    data = {
        "email": email,
        "token": token,
        "newPassword": new_password
    }

    response = api_post(
        "/api/authentication/reset-password",
        data,
        auth_required=False
    )

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        return True, None

    try:
        return False, response.json()
    except Exception:
        return False, response.text