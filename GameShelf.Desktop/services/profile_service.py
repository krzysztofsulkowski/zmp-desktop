import os
import requests

from config import API_URL, VERIFY_SSL
from services.response_helpers import error_message
from services.session import get_token

REQUEST_TIMEOUT = 10


def update_profile(username, bio, avatar_path=None):
    token = get_token()

    if not token:
        return False, "Brak tokena użytkownika."

    avatar_file = None

    try:
        files = build_profile_files(username, bio, avatar_path)
        avatar_file = get_avatar_file(files)
        response = requests.put(
            f"{API_URL}/api/authentication/update-profile",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
            verify=VERIFY_SSL,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            return True, None

        return False, error_message(response, f"Status: {response.status_code}, treść: {response.text}")
    except requests.RequestException as request_error:
        return False, str(request_error)
    finally:
        if avatar_file:
            avatar_file.close()


def build_profile_files(username, bio, avatar_path):
    files = [
        ("Username", (None, username)),
        ("Bio", (None, bio)),
    ]

    if avatar_path:
        avatar_file = open(avatar_path, "rb")
        files.append(
            (
                "Avatar",
                (
                    os.path.basename(avatar_path),
                    avatar_file,
                    "application/octet-stream",
                ),
            )
        )

    return files


def get_avatar_file(files):
    for field_name, file_data in files:
        if field_name == "Avatar":
            return file_data[1]

    return None
