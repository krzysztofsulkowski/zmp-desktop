import os
import sys
from pathlib import Path

APP_NAME = "GameShelf"


def get_runtime_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[1]


def get_bundle_dir():
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parents[1]


def get_resource_path(*parts):
    return get_bundle_dir().joinpath(*parts)


def get_user_data_dir():
    if sys.platform.startswith("win"):
        base_dir = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

    data_dir = base_dir / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_user_data_file(filename):
    return get_user_data_dir() / filename
