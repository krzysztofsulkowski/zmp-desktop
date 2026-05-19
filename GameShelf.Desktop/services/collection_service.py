from services.api_client import api_get, api_post, api_put, api_delete
from models.game import Game


def get_my_collection():
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

    if response.status_code != 200:
        return []

    try:
        result = response.json()
    except Exception:
        return []

    games = []

    for collection in result.get("data", []):
        for game in collection.get("games", []):
            games.append(
                Game(
                    game_id=game.get("gameId"),
                    title=game.get("title"),
                    genre=game.get("genreName"),
                    platform=game.get("platformName"),
                    image_url=game.get("imageUrl"),
                    collection_id=collection.get("collectionId")
                )
            )

    return games


def get_collections_lookup():
    response = api_get("/api/collections/lookup")

    if response.status_code != 200:
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

    return response.status_code == 200


def update_collection(collection_id, name, is_public=True):
    data = {
        "id": collection_id,
        "name": name,
        "isPublic": is_public
    }

    response = api_put("/api/collections/update", data)

    return response.status_code == 200


def delete_collection(collection_id):
    response = api_delete(f"/api/collections/delete/{collection_id}")

    return response.status_code == 200