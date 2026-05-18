import requests

from config import API_URL
from services.session import get_token


def get_headers():
    token = get_token()

    return {
        "Authorization": f"Bearer {token}"
    }


def api_get(endpoint):
    url = f"{API_URL}{endpoint}"

    return requests.get(
        url,
        headers=get_headers(),
        verify=False
    )


def api_post(endpoint, data=None):
    url = f"{API_URL}{endpoint}"

    return requests.post(
        url,
        json=data,
        headers=get_headers(),
        verify=False
    )


def api_put(endpoint, data=None):
    url = f"{API_URL}{endpoint}"

    return requests.put(
        url,
        json=data,
        headers=get_headers(),
        verify=False
    )


def api_delete(endpoint):
    url = f"{API_URL}{endpoint}"

    return requests.delete(
        url,
        headers=get_headers(),
        verify=False
    )


def get_me():
    return api_get("/api/authentication/me")