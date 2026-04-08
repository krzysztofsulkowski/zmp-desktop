from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from services.auth_service import login
from services.session import set_token
from views.main_view import MainView


class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GameShelf - Login")

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        self.status_label = QLabel("")

        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        token = login(email, password)

        if not token:
            self.status_label.setText("Login failed")
            return

        set_token(token)
        self.status_label.setText("Login successful")

        self.main_view = MainView()
        self.main_view.show()

        self.close()