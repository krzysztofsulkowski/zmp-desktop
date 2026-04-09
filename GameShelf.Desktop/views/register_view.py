from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)
from services.auth_service import register


class RegisterView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.setWindowTitle("Register")

        layout = QVBoxLayout()

        self.title = QLabel("Rejestracja")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("adres e-mail")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("nazwa użytkownika")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("hasło")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setPlaceholderText("powtórz hasło")
        self.repeat_password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Zarejestruj się")
        self.google_button = QPushButton("Kontynuuj przez Google")
        self.login_link = QPushButton("Masz już konto? Zaloguj się")

        layout.addWidget(self.title)
        layout.addWidget(self.email_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.repeat_password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.google_button)
        layout.addWidget(self.login_link)

        self.setLayout(layout)

        self.register_button.clicked.connect(self.handle_register)
        self.login_link.clicked.connect(self.controller.show_login)

    def handle_register(self):
        email = self.email_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()

        if not email or not username or not password or not repeat_password:
            QMessageBox.warning(self, "Błąd", "Wszystkie pola są wymagane.")
            return

        if password != repeat_password:
            QMessageBox.warning(self, "Błąd", "Hasła nie są takie same.")
            return

        success, error = register(email, username, password)

        if success:
            QMessageBox.information(self, "Sukces", "Konto zostało utworzone.")
            self.controller.show_login()
        else:
            QMessageBox.warning(self, "Błąd", error)