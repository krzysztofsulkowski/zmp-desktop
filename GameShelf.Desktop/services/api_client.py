import requests

from config import API_URL, VERIFY_SSL
from services.session import get_token, clear_token

REQUEST_TIMEOUT = 10


def build_url(endpoint):
    return f"{API_URL}{endpoint}"


def get_headers(auth_required=True):
    headers = {}

    if not auth_required:
        return headers

    token = get_token()

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def handle_unauthorized(response):
    if response is not None and response.status_code == 401:
        clear_token()


def api_get(endpoint, auth_required=True):
    try:
        response = requests.get(
            build_url(endpoint),
            headers=get_headers(auth_required),
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT
        )

        handle_unauthorized(response)

        return response
    except requests.RequestException:
        return None


def api_post(endpoint, data=None, auth_required=True):
    try:
        response = requests.post(
            build_url(endpoint),
            json=data,
            headers=get_headers(auth_required),
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT
        )

        handle_unauthorized(response)

        return response
    except requests.RequestException:
        return None


def api_put(endpoint, data=None, auth_required=True):
    try:
        response = requests.put(
            build_url(endpoint),
            json=data,
            headers=get_headers(auth_required),
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT
        )

        handle_unauthorized(response)

        return response
    except requests.RequestException:
        return None


def api_delete(endpoint, auth_required=True):
    try:
        response = requests.delete(
            build_url(endpoint),
            headers=get_headers(auth_required),
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT
        )

        handle_unauthorized(response)

        return response
    except requests.RequestException:
        return None


def get_me():
    return api_get("/api/authentication/me")