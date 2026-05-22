import json
import os
import sys
from pathlib import Path

APP_NAME = "GameShelfDesktop"
DEFAULT_SETTINGS = {
    "start_with_system": False
}


def get_settings_file():
    if sys.platform.startswith("win"):
        base_dir = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

    settings_dir = base_dir / APP_NAME
    settings_dir.mkdir(parents=True, exist_ok=True)
    return settings_dir / "app_settings.json"


SETTINGS_FILE = get_settings_file()


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
