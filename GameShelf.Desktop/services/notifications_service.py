import json
from pathlib import Path

from services.friends_service import get_pending_requests


class NotificationsService:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)

    def load_read_notifications(self):
        if not self.storage_path.exists():
            return set()

        try:
            with open(self.storage_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception:
            return set()

        if not isinstance(data, list):
            return set()

        return set(data)

    def save_read_notifications(self, notification_ids):
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(sorted(notification_ids), file, ensure_ascii=False, indent=2)

    def get_notifications(self):
        notifications = []

        for request in get_pending_requests():
            username = request.get("userName") or request.get("username") or "Nieznany użytkownik"
            user_id = request.get("userId") or request.get("id") or username

            notifications.append({
                "id": f"friend_request:{user_id}",
                "title": "Zaproszenie do znajomych",
                "content": f"Użytkownik {username} wysłał Ci zaproszenie do znajomych."
            })

        return notifications
