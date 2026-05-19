from services.api_client import api_get


def get_my_library_statistics():
    response = api_get("/api/statistics/my-library")

    if response.status_code != 200:
        return None

    return response.json()


def get_global_statistics():
    response = api_get("/api/statistics/global")

    if response.status_code != 200:
        return None

    return response.json()