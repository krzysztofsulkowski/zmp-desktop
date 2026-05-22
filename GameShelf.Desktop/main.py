import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from controllers.app_controller import AppController
from utils.app_identity import APP_NAME, get_app_icon, setup_windows_app_user_model_id

BASE_DIR = Path(__file__).resolve().parent
STYLE_FILES = (
    "theme.qss",
    "landing_view.qss",
    "auth.qss",
    "main.qss",
    "dialogs.qss",
    "cards.qss",
    "stats.qss",
    "friends.qss",
    "settings.qss",
    "notifications.qss",
    "chat.qss",
)


def load_styles(app):
    styles = []

    for style_file in STYLE_FILES:
        file_path = BASE_DIR / "styles" / style_file

        if file_path.exists():
            styles.append(file_path.read_text(encoding="utf-8"))

    app.setStyleSheet("\n".join(styles))


def main():
    setup_windows_app_user_model_id()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setWindowIcon(get_app_icon())
    load_styles(app)

    controller = AppController()
    controller.show_landing()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
