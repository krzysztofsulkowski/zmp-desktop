from urllib.parse import quote

from services.api_client import api_delete, api_get, api_post
from services.response_helpers import error_message, is_success, response_data, response_json


def get_my_friends():
    response = api_get("/api/friends/my-friends")

    if not is_success(response):
        return []

    return response_json(response, []) or []


def search_users(search_value):
    data = {
        "draw": 1,
        "start": 0,
        "length": 20,
        "searchValue": search_value,
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {},
    }

    response = api_post("/api/friends/search", data)

    if not is_success(response):
        return []

    return response_data(response, []) or []


def add_friend_by_username(username):
    response = api_post(f"/api/friends/add-by-username/{quote(username)}")

    if response is None:
        return False, "Brak połączenia z API."

    if is_success(response):
        return True, "Zaproszenie zostało wysłane."

    return False, error_message(response, "Nie udało się wysłać zaproszenia.")


def get_pending_requests():
    response = api_get("/api/friends/pending-requests")

    if not is_success(response):
        return []

    return response_json(response, []) or []


def accept_friend_request(requester_id):
    response = api_post(f"/api/friends/accept/{requester_id}")

    if response is None:
        return False, "Brak połączenia z API."

    if is_success(response):
        return True, "Zaproszenie zaakceptowane."

    return False, error_message(response, "Nie udało się zaakceptować zaproszenia.")


def reject_or_remove_friend(friend_id):
    response = api_delete(f"/api/friends/reject-or-remove/{friend_id}")

    if response is None:
        return False, "Brak połączenia z API."

    if is_success(response):
        return True, "Operacja zakończona."

    return False, error_message(response, "Nie udało się wykonać operacji.")


def get_friend_collections_with_games(friend_id):
    response = api_get(f"/api/friends/{friend_id}/collections-with-games")

    if not is_success(response):
        return []

    return response_json(response, []) or []


def compare_with_friend(friend_id):
    response = api_get(f"/api/friends/compare/{friend_id}")

    if not is_success(response):
        return []

    return response_json(response, []) or []
