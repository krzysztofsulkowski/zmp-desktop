import json
from pathlib import Path

STORE_PATH = Path("share_codes.json")


def load_share_codes():
    if not STORE_PATH.exists():
        return {}

    try:
        with open(STORE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_share_code(collection_id, share_code):
    if not collection_id or not share_code:
        return

    data = load_share_codes()
    data[str(collection_id)] = share_code

    with open(STORE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_share_code(collection_id):
    data = load_share_codes()
    return data.get(str(collection_id))