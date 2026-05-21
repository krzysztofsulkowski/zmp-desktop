from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QFrame,
    QSizePolicy
)

from services.app_settings_service import (
    load_settings,
    save_settings,
    set_start_with_system
)


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("settingsView")

        self.settings = load_settings()

        self.title_label = QLabel("Ustawienia")
        self.title_label.setObjectName("settingsPageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_with_system_checkbox = QCheckBox(
            "Uruchamiaj aplikację przy starcie systemu"
        )
        self.start_with_system_checkbox.setObjectName("settingsCheckbox")
        self.start_with_system_checkbox.setChecked(
            self.settings.get("start_with_system", False)
        )

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(42, 24, 42, 32)
        outer_layout.setSpacing(24)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("settingsContentFrame")
        self.content_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(34, 22, 34, 26)
        content_layout.setSpacing(26)

        option_card = QFrame()
        option_card.setObjectName("settingsOptionCard")

        option_layout = QHBoxLayout(option_card)
        option_layout.setContentsMargins(24, 22, 24, 22)
        option_layout.setSpacing(12)
        option_layout.addWidget(self.start_with_system_checkbox)
        option_layout.addStretch()

        content_layout.addWidget(self.title_label)
        content_layout.addWidget(option_card)
        content_layout.addStretch()

        outer_layout.addWidget(self.content_frame)
        self.setLayout(outer_layout)

    def connect_signals(self):
        self.start_with_system_checkbox.stateChanged.connect(
            self.save_local_settings
        )

    def save_local_settings(self):
        self.settings["start_with_system"] = (
            self.start_with_system_checkbox.isChecked()
        )

        save_settings(self.settings)

        set_start_with_system(
            self.settings["start_with_system"]
        )

