import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from controllers.app_controller import AppController


def load_styles(app):
    base_dir = Path(__file__).resolve().parent

    style_files = [
        base_dir / "styles" / "theme.qss",
        base_dir / "styles" / "landing_view.qss",
        base_dir / "styles" / "auth.qss",
        base_dir / "styles" / "main.qss",
        base_dir / "styles" / "dialogs.qss",
        base_dir / "styles" / "cards.qss",
        base_dir / "styles" / "stats.qss",
    ]

    combined_styles = ""

    for file_path in style_files:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                combined_styles += file.read() + "\n"

    app.setStyleSheet(combined_styles)


def main():
    app = QApplication(sys.argv)

    load_styles(app)

    controller = AppController()
    controller.show_landing()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()