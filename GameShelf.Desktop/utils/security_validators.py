import re
from pathlib import Path

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{3,40}$")
MAX_BIO_LENGTH = 500
MAX_MESSAGE_LENGTH = 1000
MAX_GROUP_NAME_LENGTH = 80
MAX_AVATAR_SIZE_BYTES = 2 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def validate_email(email):
    return bool(email and EMAIL_PATTERN.match(email.strip()))


def validate_password(password):
    if not password or len(password) < 8:
        return False, "Hasło musi mieć co najmniej 8 znaków."

    if not re.search(r"[A-Z]", password):
        return False, "Hasło musi zawierać co najmniej jedną wielką literę."

    if not re.search(r"[a-z]", password):
        return False, "Hasło musi zawierać co najmniej jedną małą literę."

    if not re.search(r"\d", password):
        return False, "Hasło musi zawierać co najmniej jedną cyfrę."

    return True, None


def validate_username(username):
    if not username:
        return False, "Nazwa użytkownika jest wymagana."

    if not USERNAME_PATTERN.match(username):
        return False, "Nazwa użytkownika musi mieć 3-40 znaków i może zawierać litery, cyfry, kropkę, podkreślnik albo myślnik."

    return True, None


def validate_bio(bio):
    if len(bio or "") > MAX_BIO_LENGTH:
        return False, f"Bio może mieć maksymalnie {MAX_BIO_LENGTH} znaków."

    return True, None


def validate_message(message):
    if not message:
        return False, "Wpisz treść wiadomości."

    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Wiadomość może mieć maksymalnie {MAX_MESSAGE_LENGTH} znaków."

    return True, None


def validate_group_name(group_name):
    if len(group_name or "") > MAX_GROUP_NAME_LENGTH:
        return False, f"Nazwa grupy może mieć maksymalnie {MAX_GROUP_NAME_LENGTH} znaków."

    return True, None


def validate_avatar_file(file_path):
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        return False, "Wybrany plik avatara nie istnieje."

    if path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        return False, "Avatar musi być plikiem PNG, JPG, JPEG albo WEBP."

    if path.stat().st_size > MAX_AVATAR_SIZE_BYTES:
        return False, "Avatar może mieć maksymalnie 2 MB."

    return True, None
