from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from services.auth_service import login
from services.session import set_token


class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("GameShelf - Login")

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.forgot_password_button = QPushButton("Nie pamiętam hasła")

        self.login_button = QPushButton("Login")

        self.google_login_button = QPushButton("Kontynuuj przez Google")

        self.register_link_button = QPushButton("Nie posiadasz konta? Zarejestruj się")

        self.status_label = QLabel("")

        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.forgot_password_button)
        layout.addWidget(self.login_button)
        layout.addWidget(self.google_login_button)
        layout.addWidget(self.register_link_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.handle_login)
        self.forgot_password_button.clicked.connect(self.controller.show_forgot_password)
        self.register_link_button.clicked.connect(self.controller.show_register)
        self.google_login_button.clicked.connect(self.handle_google_login)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        token = login(email, password)

        if not token:
            self.status_label.setText("Login failed")
            return

        set_token(token)
        self.status_label.setText("Login successful")
        self.controller.show_main()

    def handle_google_login(self):
        self.status_label.setText("Google login not implemented yet")