import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from controllers.app_controller import AppController


def load_stylesheet(app):
    base_dir = Path(__file__).resolve().parent
    stylesheet_path = base_dir / "styles" / "theme.qss"

    if stylesheet_path.exists():
        with open(stylesheet_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


def main():
    app = QApplication(sys.argv)

    load_stylesheet(app)

    controller = AppController()
    controller.show_landing()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()