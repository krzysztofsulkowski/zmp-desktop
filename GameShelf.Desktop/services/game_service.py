from services.api_client import api_post, api_delete


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

    if response.status_code != 200:
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

    return response.status_code == 200


def remove_game_from_collection(game_id):
    response = api_delete(f"/api/games/remove-from-collection/{game_id}")

    return response.status_code == 200