import requests
from config import API_URL
from services.session import get_token


def get_available_games():
    url = f"{API_URL}/api/games/available-table"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "draw": 1,
        "start": 0,
        "length": 100,
        "searchValue": "",
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {}
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        verify=False
    )

    if response.status_code != 200:
        return []

    result = response.json()
    return result.get("data", [])


def add_game_to_collection(game_id, collection_id):
    url = f"{API_URL}/api/games/add-to-collection/{game_id}?collectionId={collection_id}"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        url,
        headers=headers,
        verify=False
    )

    print("ADD GAME STATUS:", response.status_code)
    print("ADD GAME TEXT:", response.text)

    return response.status_code == 200