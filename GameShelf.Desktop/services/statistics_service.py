from services.api_client import api_get
from services.response_helpers import is_success, response_json


def get_my_library_statistics():
    response = api_get("/api/statistics/my-library")

    if not is_success(response):
        return None

    return response_json(response)


def get_global_statistics():
    response = api_get("/api/statistics/global")

    if not is_success(response):
        return None

    return response_json(response)
