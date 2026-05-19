import json
import sys
import winreg
from pathlib import Path

SETTINGS_FILE = Path("app_settings.json")
APP_NAME = "GameShelfDesktop"


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


def set_start_with_system(enabled):
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        registry_path,
        0,
        winreg.KEY_SET_VALUE
    ) as key:
        if enabled:
            app_path = sys.executable
            winreg.SetValueEx(
                key,
                APP_NAME,
                0,
                winreg.REG_SZ,
                f'"{app_path}"'
            )
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass