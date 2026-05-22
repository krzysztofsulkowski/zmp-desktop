import sys
from pathlib import Path

from PySide6.QtGui import QIcon

APP_NAME = "GameShelf"
APP_USER_MODEL_ID = "GameShelf.Desktop.App"
BASE_DIR = Path(__file__).resolve().parent.parent
APP_ICON_PATH = BASE_DIR / "assets" / "logo.svg"


def get_app_icon():
    return QIcon(str(APP_ICON_PATH))


def setup_windows_app_user_model_id():
    if not sys.platform.startswith("win"):
        return

    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            APP_USER_MODEL_ID
        )
    except (AttributeError, OSError):
        return


def get_window_title(title=None):
    if not title:
        return APP_NAME

    return f"{APP_NAME} - {title}"
