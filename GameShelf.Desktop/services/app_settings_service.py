import json
from pathlib import Path

SETTINGS_FILE = Path("app_settings.json")


def load_settings():
    if not SETTINGS_FILE.exists():
        return {
            "start_with_system": False
        }

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)