from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from services.api_client import get_me
from services.session import clear_token


class ProfileView(QWidget):
    def __init__(self, on_logout):
        super().__init__()

        self.on_logout = on_logout

        self.title_label = QLabel("Profil użytkownika")
        self.email_label = QLabel("Email: ładowanie...")
        self.username_label = QLabel("Nazwa użytkownika: ładowanie...")
        self.logout_button = QPushButton("Wyloguj")

        self.setup_ui()
        self.connect_signals()
        self.load_user_data()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(self.title_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.username_label)
        layout.addStretch()
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def connect_signals(self):
        self.logout_button.clicked.connect(self.logout)

    def load_user_data(self):
        response = get_me()

        if response.status_code != 200:
            self.email_label.setText("Email: brak danych")
            self.username_label.setText("Nazwa użytkownika: brak danych")
            return

        user_data = response.json()

        email = user_data.get("email", "brak danych")
        username = user_data.get("userName", "brak danych")

        self.email_label.setText(f"Email: {email}")
        self.username_label.setText(f"Nazwa użytkownika: {username}")

    def logout(self):
        clear_token()
        self.on_logout()