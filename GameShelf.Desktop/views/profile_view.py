import requests

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)

from config import API_URL, VERIFY_SSL
from services.api_client import get_me
from services.session import clear_token
from services.profile_service import update_profile
from views.edit_profile_dialog import EditProfileDialog


class ProfileView(QWidget):
    def __init__(self, on_logout):
        super().__init__()
        self.setObjectName("profileView")

        self.on_logout = on_logout
        self.user_data = {}

        self.title_label = QLabel("Profil użytkownika")
        self.title_label.setObjectName("pageTitle")
        self.avatar_label = QLabel("Brak avatara")
        self.email_label = QLabel("Email: ładowanie...")
        self.username_label = QLabel("Nazwa użytkownika: ładowanie...")
        self.bio_label = QLabel("Bio: ładowanie...")
        self.edit_profile_button = QPushButton("Edytuj profil")
        self.edit_profile_button.setObjectName("secondaryButton")
        self.logout_button = QPushButton("Wyloguj")
        self.logout_button.setObjectName("dangerButton")

        self.setup_ui()
        self.connect_signals()
        self.load_user_data()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.avatar_label.setFixedSize(120, 120)
        self.avatar_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.bio_label)
        layout.addWidget(self.edit_profile_button)
        layout.addStretch()
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def connect_signals(self):
        self.logout_button.clicked.connect(self.logout)
        self.edit_profile_button.clicked.connect(self.open_edit_profile_dialog)

    def load_user_data(self):
        response = get_me()

        if response is None or response.status_code != 200:
            self.email_label.setText("Email: brak danych")
            self.username_label.setText("Nazwa użytkownika: brak danych")
            self.bio_label.setText("Bio: brak danych")
            self.avatar_label.setText("Brak avatara")
            return

        self.user_data = response.json()

        email = self.user_data.get("email", "brak danych")
        username = self.user_data.get("userName", "brak danych")
        bio = self.user_data.get("bio", "brak danych")
        avatar_url = self.user_data.get("avatarUrl")

        self.email_label.setText(f"Email: {email}")
        self.username_label.setText(f"Nazwa użytkownika: {username}")
        self.bio_label.setText(f"Bio: {bio or 'brak danych'}")

        self.load_avatar(avatar_url)

    def load_avatar(self, avatar_url):
        if not avatar_url:
            self.avatar_label.setText("Brak avatara")
            return

        if avatar_url.startswith("/"):
            avatar_url = f"{API_URL}{avatar_url}"

        try:
            response = requests.get(
                avatar_url,
                verify=VERIFY_SSL,
                timeout=10
            )

            if response.status_code != 200:
                self.avatar_label.setText("Brak avatara")
                return

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            scaled_pixmap = pixmap.scaled(
                120,
                120,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.avatar_label.setPixmap(scaled_pixmap)
        except requests.RequestException:
            self.avatar_label.setText("Brak avatara")

    def open_edit_profile_dialog(self):
        username = self.user_data.get("userName", "")
        bio = self.user_data.get("bio", "")

        dialog = EditProfileDialog(username, bio)
        result = dialog.exec()

        if result != EditProfileDialog.Accepted:
            return

        success, error = update_profile(
            dialog.get_username(),
            dialog.get_bio(),
            dialog.get_avatar_path()
        )

        if not success:
            QMessageBox.warning(
                self,
                "GameShelf",
                f"Nie udało się zaktualizować profilu.\n\n{error}"
            )
            return

        QMessageBox.information(
            self,
            "GameShelf",
            "Profil został zaktualizowany."
        )

        self.load_user_data()

    def logout(self):
        clear_token()
        self.on_logout()