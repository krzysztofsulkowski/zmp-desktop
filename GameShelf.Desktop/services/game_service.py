import requests

from config import API_URL, VERIFY_SSL
from services.api_client import REQUEST_TIMEOUT, api_delete, api_get, api_post, get_headers

AVAILABLE_GAMES_REQUEST = {
    "draw": 1,
    "start": 0,
    "length": 100,
    "searchValue": "",
    "orderColumn": 0,
    "orderDir": "asc",
    "extraFilters": {},
}


def _get_json(response, fallback):
    if response is None or response.status_code != 200:
        return fallback

    try:
        return response.json()
    except Exception:
        return fallback


def get_available_games():
    response = api_post("/api/games/available-table", AVAILABLE_GAMES_REQUEST)
    result = _get_json(response, {})
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
    return _get_json(response, [])


def get_game_platforms():
    response = api_get("/api/games/platforms")
    return _get_json(response, [])


def propose_game(title, description, genre_id, platform_id, image_path=None):
    data = {
        "title": title,
        "description": description,
        "genreId": str(genre_id),
        "platformId": str(platform_id),
    }

    try:
        return _send_game_proposal(data, image_path)
    except requests.RequestException:
        return False


def _send_game_proposal(data, image_path):
    with _open_image_file(image_path) as image_file:
        files = {"image": image_file} if image_file else None
        response = requests.post(
            f"{API_URL}/api/games/propose",
            data=data,
            files=files,
            headers=get_headers(),
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT,
        )

    return response.status_code == 200


def _open_image_file(image_path):
    if not image_path:
        return _EmptyFileContext()

    return open(image_path, "rb")


class _EmptyFileContext:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def move_game(game_id, current_collection_id, target_collection_id):
    response = api_post(
        "/api/games/move-game",
        {
            "gameId": game_id,
            "currentCollectionId": current_collection_id,
            "targetCollectionId": target_collection_id,
        },
    )

    return response is not None and response.status_code == 200


def rate_game(game_id, rating):
    response = api_post(
        "/api/games/rate",
        {
            "gameId": game_id,
            "rating": rating,
        },
    )

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        return True, None

    try:
        return False, response.json()
    except Exception:
        return False, response.text
