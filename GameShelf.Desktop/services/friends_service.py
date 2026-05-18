from services.api_client import api_get


def get_my_friends():
    response = api_get("/api/friends/my-friends")

    print("FRIENDS STATUS:", response.status_code)
    print("FRIENDS TEXT:", response.text)

    if response.status_code != 200:
        return []

    return response.json()