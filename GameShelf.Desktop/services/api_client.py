import requests

from config import API_URL, VERIFY_SSL
from services.session import get_token, clear_token

REQUEST_TIMEOUT = 10


def build_url(endpoint):
    return f"{API_URL}{endpoint}"


def get_headers(auth_required=True):
    if not auth_required:
        return {}

    token = get_token()

    if not token:
        return {}

    return {"Authorization": f"Bearer {token}"}


def handle_unauthorized(response):
    if response is not None and response.status_code == 401:
        clear_token()


def api_request(method, endpoint, data=None, auth_required=True):
    try:
        response = requests.request(
            method,
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


def api_get(endpoint, auth_required=True):
    return api_request("GET", endpoint, auth_required=auth_required)


def api_post(endpoint, data=None, auth_required=True):
    return api_request("POST", endpoint, data, auth_required)


def api_put(endpoint, data=None, auth_required=True):
    return api_request("PUT", endpoint, data, auth_required)


def api_delete(endpoint, auth_required=True):
    return api_request("DELETE", endpoint, auth_required=auth_required)


def get_me():
    return api_get("/api/authentication/me")
