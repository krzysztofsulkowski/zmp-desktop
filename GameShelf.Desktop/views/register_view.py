from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFrame

from services.auth_service import register


class RegisterView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.setWindowTitle("Register")
        self.setObjectName("authPage")

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setContentsMargins(32, 32, 32, 32)

        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(460)

        layout = QVBoxLayout()
        layout.setContentsMargins(38, 34, 38, 34)
        layout.setSpacing(14)

        self.logo_label = QLabel("GameShelf")
        self.logo_label.setObjectName("authLogo")
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.title = QLabel("Rejestracja")
        self.title.setObjectName("authTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel("Utwórz konto i zacznij porządkować swoje gry")
        self.subtitle_label.setObjectName("authSubtitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Adres e-mail")
        self.email_input.setMinimumHeight(44)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")
        self.username_input.setMinimumHeight(44)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(44)

        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setPlaceholderText("Powtórz hasło")
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        self.repeat_password_input.setMinimumHeight(44)

        self.register_button = QPushButton("Zarejestruj się")
        self.register_button.setObjectName("authPrimaryButton")
        self.register_button.setMinimumHeight(44)

        self.google_button = QPushButton("Kontynuuj przez Google")
        self.google_button.setObjectName("authSecondaryButton")
        self.google_button.setMinimumHeight(44)

        self.login_link = QPushButton("Masz już konto? Zaloguj się")
        self.login_link.setObjectName("authLinkButton")

        layout.addWidget(self.logo_label)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle_label)
        layout.addSpacing(10)
        layout.addWidget(self.email_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.repeat_password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.google_button)
        layout.addWidget(self.login_link)

        card.setLayout(layout)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

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
