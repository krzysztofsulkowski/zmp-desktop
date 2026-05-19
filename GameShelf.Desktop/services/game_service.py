import requests

from config import API_URL, VERIFY_SSL
from services.api_client import api_get, api_post, api_delete
from services.session import get_token

REQUEST_TIMEOUT = 10


def get_available_games():
    data = {
        "draw": 1,
        "start": 0,
        "length": 100,
        "searchValue": "",
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {}
    }

    response = api_post("/api/games/available-table", data)

    if response is None or response.status_code != 200:
        return []

    try:
        result = response.json()
    except Exception:
        return []

    return result.get("data", [])


def add_game_to_collection(game_id, collection_id):
    response = api_post(
        f"/api/games/add-to-collection/{game_id}?collectionId={collection_id}"
    )

    return response is not None and response.status_code == 200


def remove_game_from_collection(game_id):
    response = api_delete(f"/api/games/remove-from-collection/{game_id}")

    return response is not None and response.status_code == 200


def get_game_genres():
    response = api_get("/api/games/genres")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def get_game_platforms():
    response = api_get("/api/games/platforms")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def propose_game(title, description, genre_id, platform_id, image_path=None):
    url = f"{API_URL}/api/games/propose"
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "title": title,
        "description": description,
        "genreId": str(genre_id),
        "platformId": str(platform_id)
    }

    files = {}

    try:
        if image_path:
            files["image"] = open(image_path, "rb")

        response = requests.post(
            url,
            data=data,
            files=files if files else None,
            headers=headers,
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT
        )

        return response.status_code == 200
    except requests.RequestException:
        return False
    finally:
        if "image" in files:
            files["image"].close()

def move_game(game_id, current_collection_id, target_collection_id):
    data = {
        "gameId": game_id,
        "currentCollectionId": current_collection_id,
        "targetCollectionId": target_collection_id
    }

    response = api_post("/api/games/move-game", data)

    return response is not None and response.status_code == 200

def rate_game(game_id, rating):
    data = {
        "gameId": game_id,
        "rating": rating
    }

    response = api_post("/api/games/rate", data)

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        return True, None

    try:
        return False, response.json()
    except Exception:
        return False, response.text