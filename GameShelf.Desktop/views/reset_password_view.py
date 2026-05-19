from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from services.auth_service import reset_password


class ResetPasswordView(QWidget):
    def __init__(self, on_back_to_login):
        super().__init__()

        self.on_back_to_login = on_back_to_login

        self.setWindowTitle("Ustaw nowe hasło")

        self.email_input = QLineEdit()
        self.token_input = QLineEdit()
        self.password_input = QLineEdit()

        self.password_input.setEchoMode(QLineEdit.Password)

        self.reset_button = QPushButton("Ustaw nowe hasło")
        self.back_button = QPushButton("Powrót do logowania")

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Token resetujący"))
        layout.addWidget(self.token_input)

        layout.addWidget(QLabel("Nowe hasło"))
        layout.addWidget(self.password_input)

        layout.addWidget(self.reset_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def connect_signals(self):
        self.reset_button.clicked.connect(self.handle_reset_password)
        self.back_button.clicked.connect(self.on_back_to_login)

    def handle_reset_password(self):
        email = self.email_input.text().strip()
        token = self.token_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not token or not password:
            QMessageBox.warning(
                self,
                "GameShelf",
                "Wszystkie pola są wymagane."
            )
            return

        success, error = reset_password(
            email,
            token,
            password
        )

        if not success:
            QMessageBox.warning(
                self,
                "GameShelf",
                f"Nie udało się ustawić nowego hasła.\n\n{error}"
            )
            return

        QMessageBox.information(
            self,
            "GameShelf",
            "Hasło zostało zmienione."
        )

        self.on_back_to_login()