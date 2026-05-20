from services.api_client import api_get, api_post


def get_my_chats():
    response = api_get("/api/chat/my-chats")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def get_chat_messages(group_id):
    response = api_get(f"/api/chat/{group_id}/messages")

    if response is None or response.status_code != 200:
        return []

    try:
        return response.json()
    except Exception:
        return []


def create_chat(group_name, user_ids):
    data = {
        "groupName": group_name,
        "userIds": user_ids
    }

    response = api_post("/api/chat/create", data)

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        try:
            return True, response.json()
        except Exception:
            return True, None

    try:
        return False, response.json()
    except Exception:
        return False, response.text