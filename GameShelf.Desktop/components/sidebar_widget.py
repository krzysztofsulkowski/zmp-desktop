from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout


class SidebarWidget(QFrame):
    def __init__(self, assets_dir):
        super().__init__()

        self.assets_dir = Path(assets_dir)
        self.setObjectName("mainSidebar")
        self.setFixedWidth(102)

        self.setup_ui()

    def setup_ui(self):
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(12, 22, 12, 22)
        sidebar.setSpacing(18)

        self.logo_label = QLabel()
        self.logo_label.setObjectName("mainLogo")
        self.logo_label.setFixedSize(78, 52)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.set_logo()

        self.profile_button = self.create_icon_button("ProfileIcon.svg")
        self.home_button = self.create_icon_button("HomeIcon.svg")
        self.stats_button = self.create_icon_button("StatsIcon.svg")
        self.friends_button = self.create_icon_button("FriendsIcon.svg")
        self.chat_button = self.create_icon_button("ChatIcon.svg")
        self.global_stats_button = self.create_icon_button("GlobalStatsIcon.svg")
        self.notifications_button = self.create_icon_button("NotificationsIcon.svg")
        self.settings_button = self.create_icon_button("SettingsIcon.svg")
        self.logout_button = self.create_icon_button("LogOutIcon.svg")

        sidebar.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        sidebar.addSpacing(20)
        sidebar.addWidget(self.profile_button, alignment=Qt.AlignCenter)
        sidebar.addWidget(self.home_button, alignment=Qt.AlignCenter)
        sidebar.addWidget(self.stats_button, alignment=Qt.AlignCenter)
        sidebar.addWidget(self.friends_button, alignment=Qt.AlignCenter)
        sidebar.addWidget(self.chat_button, alignment=Qt.AlignCenter)
        sidebar.addWidget(self.global_stats_button, alignment=Qt.AlignCenter)
        sidebar.addWidget(self.notifications_button, alignment=Qt.AlignCenter)
        sidebar.addWidget(self.settings_button, alignment=Qt.AlignCenter)
        sidebar.addStretch()
        sidebar.addWidget(self.logout_button, alignment=Qt.AlignCenter)

        self.setLayout(sidebar)

    def set_logo(self):
        logo_pixmap = QPixmap(str(self.assets_dir / "logo.svg"))

        if logo_pixmap.isNull():
            self.logo_label.setText("GS")
            return

        self.logo_label.setPixmap(
            logo_pixmap.scaled(
                76,
                48,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def create_icon_button(self, icon_name):
        button = QPushButton()
        button.setObjectName("mainSidebarButton")
        button.setFixedSize(52, 52)
        button.setIcon(QIcon(str(self.assets_dir / icon_name)))
        button.setIconSize(QSize(30, 30))
        return button
