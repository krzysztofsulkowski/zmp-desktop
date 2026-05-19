from services.api_client import api_get, api_post, api_delete


def get_my_friends():
    response = api_get("/api/friends/my-friends")

    if response.status_code != 200:
        return []

    return response.json()


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

    if response.status_code != 200:
        return []

    result = response.json()
    return result.get("data", [])


def add_friend_by_username(username):
    response = api_post(f"/api/friends/add-by-username/{username}")

    if response.status_code == 200:
        return True, "Zaproszenie zostało wysłane."

    try:
        error_data = response.json()
        return False, error_data.get("detail", "Nie udało się wysłać zaproszenia.")
    except Exception:
        return False, "Nie udało się wysłać zaproszenia."


def get_pending_requests():
    response = api_get("/api/friends/pending-requests")

    if response.status_code != 200:
        return []

    return response.json()


def accept_friend_request(requester_id):
    response = api_post(f"/api/friends/accept/{requester_id}")

    if response.status_code == 200:
        return True, "Zaproszenie zaakceptowane."

    try:
        error_data = response.json()
        return False, error_data.get("detail", "Nie udało się zaakceptować zaproszenia.")
    except Exception:
        return False, "Nie udało się zaakceptować zaproszenia."


def reject_or_remove_friend(friend_id):
    response = api_delete(f"/api/friends/reject-or-remove/{friend_id}")

    if response.status_code == 200:
        return True, "Zaproszenie odrzucone."

    try:
        error_data = response.json()
        return False, error_data.get("detail", "Nie udało się odrzucić zaproszenia.")
    except Exception:
        return False, "Nie udało się odrzucić zaproszenia."


def get_friend_collections_with_games(friend_id):
    response = api_get(f"/api/friends/{friend_id}/collections-with-games")

    if response.status_code != 200:
        return []

    return response.json()


def compare_with_friend(friend_id):
    response = api_get(f"/api/friends/compare/{friend_id}")

    if response.status_code != 200:
        return []

    return response.json()