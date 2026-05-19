from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox
)

from services.auth_service import get_user_profile
from services.app_settings_service import (
    load_settings,
    save_settings,
    set_start_with_system
)

from config import API_URL


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = load_settings()

        layout = QVBoxLayout()

        self.title_label = QLabel("Ustawienia")
        self.api_url_label = QLabel(f"API URL: {API_URL}")

        self.username_label = QLabel()
        self.email_label = QLabel()

        self.start_with_system_checkbox = QCheckBox(
            "Uruchamiaj aplikację przy starcie systemu"
        )

        self.start_with_system_checkbox.setChecked(
            self.settings.get("start_with_system", False)
        )

        self.refresh_button = QPushButton("Odśwież dane użytkownika")

        layout.addWidget(self.title_label)
        layout.addWidget(self.api_url_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.start_with_system_checkbox)
        layout.addWidget(self.refresh_button)
        layout.addStretch()

        self.setLayout(layout)

        self.refresh_button.clicked.connect(self.load_user_profile)

        self.start_with_system_checkbox.stateChanged.connect(
            self.save_local_settings
        )

        self.load_user_profile()

    def load_user_profile(self):
        profile = get_user_profile()

        username = profile.get("userName", "Brak danych")
        email = profile.get("email", "Brak danych")

        self.username_label.setText(f"Nazwa użytkownika: {username}")
        self.email_label.setText(f"E-mail: {email}")

    def save_local_settings(self):
        self.settings["start_with_system"] = (
            self.start_with_system_checkbox.isChecked()
        )

        save_settings(self.settings)

        set_start_with_system(
            self.settings["start_with_system"]
        )