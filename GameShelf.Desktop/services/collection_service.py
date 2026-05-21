from services.api_client import api_get, api_post, api_put, api_delete
from models.game import Game
from services.share_code_store import save_share_code


def get_available_game_images():
    data = {
        "draw": 1,
        "start": 0,
        "length": 1000,
        "searchValue": "",
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {}
    }

    response = api_post("/api/games/available-table", data)

    if response is None or response.status_code != 200:
        return {}

    try:
        result = response.json()
    except Exception:
        return {}

    images = {}

    for game in result.get("data", []):
        game_id = game.get("id")
        image_url = game.get("imageUrl")

        if game_id is not None and image_url:
            images[game_id] = image_url

    return images


def get_game_rating(game_id):
    """Fetch the average (user's own) rating for a game via API."""
    response = api_get(f"/api/games/{game_id}/average-rating")

    if response is None or response.status_code != 200:
        return None

    try:
        value = response.json()
        if value and float(value) > 0:
            return round(float(value), 1)
        return None
    except Exception:
        return None


def get_my_collection():
    game_images = get_available_game_images()

    data = {
        "draw": 1,
        "start": 0,
        "length": 50,
        "searchValue": "",
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {}
    }

    response = api_post("/api/collections/grouped-with-games", data)

    if response is None or response.status_code != 200:
        return []

    try:
        result = response.json()
    except Exception:
        return []

    games = []

    for collection in result.get("data", []):
        for game in collection.get("games", []):
            game_id = game.get("gameId")
            # API doesn't return user rating in this endpoint — fetch separately
            rating = get_game_rating(game_id)
            games.append(
                Game(
                    game_id=game_id,
                    title=game.get("title"),
                    genre=game.get("genreName"),
                    platform=game.get("platformName"),
                    image_url=game.get("imageUrl") or game_images.get(game_id),
                    collection_id=collection.get("collectionId"),
                    rating=rating
                )
            )

    return games


def get_collections_lookup():
    response = api_get("/api/collections/lookup")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def create_collection(name, is_public):
    data = {
        "id": 0,
        "name": name,
        "isPublic": is_public
    }

    response = api_post("/api/collections/create", data)

    if response is None or response.status_code != 200:
        return False

    try:
        result = response.json()
        save_share_code(result.get("id"), result.get("shareCode"))
    except Exception:
        pass

    return True


def update_collection(collection_id, name, is_public=True):
    data = {
        "id": collection_id,
        "name": name,
        "isPublic": is_public
    }

    response = api_put("/api/collections/update", data)

    return response is not None and response.status_code == 200


def delete_collection(collection_id):
    response = api_delete(f"/api/collections/delete/{collection_id}")

    return response is not None and response.status_code == 200