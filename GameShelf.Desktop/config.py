import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://localhost:8081").rstrip("/")
VERIFY_SSL = os.getenv("VERIFY_SSL", "true").lower() == "true"
WEB_REGISTER_URL = os.getenv(
    "WEB_REGISTER_URL",
    "http://localhost:5173/register"
)
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
