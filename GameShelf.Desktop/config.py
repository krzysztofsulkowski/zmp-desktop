import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

PROD_API_URL = "https://game-organizer-g3ul.onrender.com"
PROD_WEB_REGISTER_URL = "https://zmp-web.onrender.com/register"


def get_runtime_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def load_environment():
    env_paths = [
        get_runtime_dir() / ".env",
        Path.cwd() / ".env",
        Path(__file__).resolve().parent / ".env"
    ]

    loaded_paths = set()

    for env_path in env_paths:
        if env_path in loaded_paths:
            continue

        loaded_paths.add(env_path)

        if env_path.exists():
            load_dotenv(env_path, override=False)


load_environment()

API_URL = os.getenv("API_URL", PROD_API_URL).rstrip("/")
VERIFY_SSL = os.getenv("VERIFY_SSL", "true").lower() == "true"
WEB_REGISTER_URL = os.getenv(
    "WEB_REGISTER_URL",
    PROD_WEB_REGISTER_URL
).rstrip("/")
CHAT_HUB_URL = os.getenv(
    "CHAT_HUB_URL",
    f"{API_URL}/chatHub"
).rstrip("/")


def is_local_api_url():
    hostname = urlparse(API_URL).hostname or ""
    return hostname in {"localhost", "127.0.0.1", "::1"}


def is_https_enabled():
    return urlparse(API_URL).scheme == "https"


def is_secure_api_configuration():
    return is_https_enabled() and (VERIFY_SSL or is_local_api_url())
