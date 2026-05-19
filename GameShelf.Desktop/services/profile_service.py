import os
import requests

from config import API_URL, VERIFY_SSL
from services.session import get_token

REQUEST_TIMEOUT = 10


def update_profile(username, bio, avatar_path=None):
    token = get_token()

    if not token:
        return False, "Brak tokena użytkownika."

    url = f"{API_URL}/api/authentication/update-profile"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = [
        ("Username", (None, username)),
        ("Bio", (None, bio))
    ]

    avatar_file = None

    try:
        if avatar_path:
            avatar_file = open(avatar_path, "rb")
            files.append(
                (
                    "Avatar",
                    (
                        os.path.basename(avatar_path),
                        avatar_file,
                        "application/octet-stream"
                    )
                )
            )

        response = requests.put(
            url,
            files=files,
            headers=headers,
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return True, None

        try:
            return False, response.json()
        except Exception:
            return False, f"Status: {response.status_code}, treść: {response.text}"

    except requests.RequestException as error:
        return False, str(error)
    finally:
        if avatar_file:
            avatar_file.close()