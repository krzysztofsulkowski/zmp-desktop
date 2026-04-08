import sys
from PySide6.QtWidgets import QApplication
from views.login_view import LoginView


def main():
    app = QApplication(sys.argv)

    window = LoginView()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()