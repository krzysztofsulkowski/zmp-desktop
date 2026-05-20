from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame

from services.auth_service import login
from services.session import set_token


class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("GameShelf - Login")
        self.setObjectName("authPage")

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setContentsMargins(32, 32, 32, 32)

        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(430)

        layout = QVBoxLayout()
        layout.setContentsMargins(38, 34, 38, 34)
        layout.setSpacing(14)

        self.logo_label = QLabel("GameShelf")
        self.logo_label.setObjectName("authLogo")
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Logowanie")
        self.title_label.setObjectName("authTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel("Zaloguj się i wróć do swojej biblioteki gier")
        self.subtitle_label.setObjectName("authSubtitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setMinimumHeight(44)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(44)

        self.forgot_password_button = QPushButton("Nie pamiętam hasła")
        self.forgot_password_button.setObjectName("authLinkButton")

        self.login_button = QPushButton("Zaloguj się")
        self.login_button.setObjectName("authPrimaryButton")
        self.login_button.setMinimumHeight(44)

        self.google_login_button = QPushButton("Kontynuuj przez Google")
        self.google_login_button.setObjectName("authSecondaryButton")
        self.google_login_button.setMinimumHeight(44)

        self.register_link_button = QPushButton("Nie posiadasz konta? Zarejestruj się")
        self.register_link_button.setObjectName("authLinkButton")

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()

        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addSpacing(10)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.forgot_password_button)
        layout.addWidget(self.login_button)
        layout.addWidget(self.google_login_button)
        layout.addWidget(self.register_link_button)
        layout.addWidget(self.status_label)

        card.setLayout(layout)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

        self.login_button.clicked.connect(self.handle_login)
        self.forgot_password_button.clicked.connect(self.controller.show_forgot_password)
        self.register_link_button.clicked.connect(self.controller.show_register)
        self.google_login_button.clicked.connect(self.handle_google_login)

    def set_status(self, text, success=False):
        self.status_label.setText(text)
        self.status_label.setObjectName("authStatusSuccess" if success else "authStatusError")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.show()

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        token = login(email, password)

        if not token:
            self.set_status("Nie udało się zalogować.")
            return

        set_token(token)
        self.set_status("Zalogowano pomyślnie.", True)
        self.controller.show_main()

    def handle_google_login(self):
        self.set_status("Logowanie przez Google nie jest jeszcze dostępne.")
