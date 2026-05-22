from services.api_client import get_me
from services.response_helpers import is_success, response_json


def get_current_user():
    response = get_me()

    if not is_success(response):
        return {}

    return response_json(response, {}) or {}
