from urllib.parse import quote

from services.api_client import api_get, api_post, api_delete


def get_my_friends():
    response = api_get("/api/friends/my-friends")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def search_users(search_value):
    data = {
        "draw": 1,
        "start": 0,
        "length": 20,
        "searchValue": search_value,
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {}
    }

    response = api_post("/api/friends/search", data)

    if response is None or response.status_code != 200:
        return []

    try:
        result = response.json()
    except Exception:
        return []

    return result.get("data", [])


def add_friend_by_username(username):
    encoded_username = quote(username)
    response = api_post(f"/api/friends/add-by-username/{encoded_username}")

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        return True, "Zaproszenie zostało wysłane."

    return False, get_error_message(response, "Nie udało się wysłać zaproszenia.")


def get_pending_requests():
    response = api_get("/api/friends/pending-requests")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def accept_friend_request(requester_id):
    response = api_post(f"/api/friends/accept/{requester_id}")

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        return True, "Zaproszenie zaakceptowane."

    return False, get_error_message(response, "Nie udało się zaakceptować zaproszenia.")


def reject_or_remove_friend(friend_id):
    response = api_delete(f"/api/friends/reject-or-remove/{friend_id}")

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        return True, "Operacja zakończona."

    return False, get_error_message(response, "Nie udało się wykonać operacji.")


def get_friend_collections_with_games(friend_id):
    response = api_get(f"/api/friends/{friend_id}/collections-with-games")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def compare_with_friend(friend_id):
    response = api_get(f"/api/friends/compare/{friend_id}")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def get_error_message(response, default_message):
    try:
        error_data = response.json()
        return error_data.get("detail") or error_data.get("title") or default_message
    except Exception:
        return default_message