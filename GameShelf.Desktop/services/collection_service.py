from config import API_URL
from services.session import get_token
from models.game import Game
import requests


def get_my_collection():
    url = f"{API_URL}/api/collections/my-collection"

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "draw": 1,
        "start": 0,
        "length": 10,
        "searchValue": "",
        "orderColumn": 0,
        "orderDir": "asc",
        "extraFilters": {}
    }

    response = requests.post(url, json=data, headers=headers, verify=False)

    result = response.json()

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