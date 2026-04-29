import requests
from config import API_URL
from services.session import get_token
from models.game import Game


def get_my_collection():
    url = f"{API_URL}/api/collections/grouped-with-games"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "draw": 1,
        "start": 0,
        "length": 50,
        "searchValue": "",
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {}
    }

    response = requests.post(url, json=data, headers=headers, verify=False)

    print("COLLECTION STATUS:", response.status_code)
    print("COLLECTION TEXT:", response.text)

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
                    image_url=game.get("imageUrl")
                )
            )

    return games

def create_collection(name, is_public):
    url = f"{API_URL}/api/collections/create"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "id": 0,
        "name": name,
        "isPublic": is_public
    }

    response = requests.post(url, json=data, headers=headers, verify=False)

    print("CREATE STATUS:", response.status_code)
    print("CREATE TEXT:", response.text)

    if response.status_code == 200:
        return True

    return False