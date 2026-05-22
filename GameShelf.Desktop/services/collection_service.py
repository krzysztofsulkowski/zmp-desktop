from models.game import Game
from services.api_client import api_delete, api_get, api_post, api_put
from services.share_code_store import save_share_code

DEFAULT_TABLE_REQUEST = {
    "draw": 1,
    "start": 0,
    "searchValue": "",
    "orderColumn": 0,
    "orderDir": "asc",
    "extraFilters": {},
}


def _build_table_request(length):
    return {**DEFAULT_TABLE_REQUEST, "length": length}


def _get_json(response, fallback):
    if response is None or response.status_code != 200:
        return fallback

    try:
        return response.json()
    except Exception:
        return fallback


def get_available_game_images():
    response = api_post("/api/games/available-table", _build_table_request(1000))
    result = _get_json(response, {})

    return {
        game.get("id"): game.get("imageUrl")
        for game in result.get("data", [])
        if game.get("id") is not None and game.get("imageUrl")
    }


def get_game_rating(game_id):
    response = api_get(f"/api/games/{game_id}/average-rating")

    if response is None or response.status_code != 200:
        return None

    try:
        rating = float(response.json())
    except Exception:
        return None

    if rating <= 0:
        return None

    return round(rating, 1)


def get_my_collection():
    game_images = get_available_game_images()
    response = api_post("/api/collections/grouped-with-games", _build_table_request(50))
    result = _get_json(response, {})

    return [
        _build_game(game, collection, game_images)
        for collection in result.get("data", [])
        for game in collection.get("games", [])
    ]


def _build_game(game, collection, game_images):
    game_id = game.get("gameId")

    return Game(
        game_id=game_id,
        title=game.get("title"),
        genre=game.get("genreName"),
        platform=game.get("platformName"),
        image_url=game.get("imageUrl") or game_images.get(game_id),
        collection_id=collection.get("collectionId"),
        rating=get_game_rating(game_id),
    )


def get_collections_lookup():
    response = api_get("/api/collections/lookup")
    return _get_json(response, [])


def get_current_collection(collection_id):
    return next(
        (collection for collection in get_collections_lookup() if collection.get("id") == collection_id),
        None,
    )


def get_sorted_collections():
    return sorted(
        get_collections_lookup(),
        key=lambda collection: collection.get("name", "").lower(),
    )


def create_collection(name, is_public):
    response = api_post(
        "/api/collections/create",
        {
            "id": 0,
            "name": name,
            "isPublic": is_public,
        },
    )

    if response is None or response.status_code != 200:
        return False

    try:
        result = response.json()
        save_share_code(result.get("id"), result.get("shareCode"))
    except Exception:
        pass

    return True


def update_collection(collection_id, name, is_public=True):
    response = api_put(
        "/api/collections/update",
        {
            "id": collection_id,
            "name": name,
            "isPublic": is_public,
        },
    )

    return response is not None and response.status_code == 200


def delete_collection(collection_id):
    response = api_delete(f"/api/collections/delete/{collection_id}")
    return response is not None and response.status_code == 200
