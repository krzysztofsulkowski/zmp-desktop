import sys
from PySide6.QtWidgets import QApplication
from controllers.app_controller import AppController


def load_stylesheet(app):
    with open("GameShelf.Desktop/styles/theme.qss", "r") as file:
        app.setStyleSheet(file.read())


def main():
    app = QApplication(sys.argv)

    load_stylesheet(app)

    controller = AppController()
    controller.show_landing()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()