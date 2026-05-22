import json
import os
import subprocess
import sys
from pathlib import Path

from utils.app_paths import APP_NAME, get_user_data_file

APP_REGISTRY_NAME = "GameShelf"
DEFAULT_SETTINGS = {
    "start_with_system": False
}


SETTINGS_FILE = get_user_data_file("app_settings.json")


def load_settings():
    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            loaded_settings = json.load(file)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()

    return {**DEFAULT_SETTINGS, **loaded_settings}


def save_settings(settings):
    safe_settings = {
        "start_with_system": bool(settings.get("start_with_system", False))
    }

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(safe_settings, file, indent=4)


def get_startup_command():
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'

    main_file = Path(__file__).resolve().parents[1] / "main.py"
    return subprocess.list2cmdline([sys.executable, str(main_file)])


def set_start_with_system(enabled):
    if not sys.platform.startswith("win"):
        return

    import winreg

    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        registry_path,
        0,
        winreg.KEY_SET_VALUE
    ) as key:
        if enabled:
            winreg.SetValueEx(
                key,
                APP_REGISTRY_NAME,
                0,
                winreg.REG_SZ,
                get_startup_command()
            )
        else:
            try:
                winreg.DeleteValue(key, APP_REGISTRY_NAME)
            except FileNotFoundError:
                pass
