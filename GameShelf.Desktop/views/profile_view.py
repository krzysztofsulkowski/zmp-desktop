import requests

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFrame,
    QSizePolicy
)

from config import API_URL, VERIFY_SSL
from services.api_client import get_me
from services.profile_service import update_profile
from views.edit_profile_dialog import EditProfileDialog


class ProfileView(QWidget):
    def __init__(self, on_logout):
        super().__init__()
        self.setObjectName("profileView")

        self.on_logout = on_logout
        self.user_data = {}

        self.title_label = QLabel("Profil użytkownika")
        self.title_label.setObjectName("profilePageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.avatar_label = QLabel("Brak avatara")
        self.avatar_label.setObjectName("profileAvatar")
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setFixedSize(150, 150)

        self.email_label = QLabel("ładowanie...")
        self.email_label.setObjectName("profileEmail")
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_label = QLabel("ładowanie...")
        self.username_label.setObjectName("profileUsername")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.edit_profile_button = QPushButton("Edytuj profil")
        self.edit_profile_button.setObjectName("profileEditButton")
        self.edit_profile_button.setFixedWidth(180)

        self.bio_title_label = QLabel("Bio")
        self.bio_title_label.setObjectName("profileBioTitle")
        self.bio_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bio_label = QLabel("ładowanie...")
        self.bio_label.setObjectName("profileBioText")
        self.bio_label.setWordWrap(True)
        self.bio_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setup_ui()
        self.connect_signals()
        self.load_user_data()

    def setup_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(42, 24, 42, 32)
        outer_layout.setSpacing(22)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("profileContentFrame")
        self.content_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(34, 22, 34, 26)
        content_layout.setSpacing(14)

        avatar_row = QHBoxLayout()
        avatar_row.setContentsMargins(0, 0, 0, 0)
        avatar_row.addStretch()
        avatar_row.addWidget(self.avatar_label)
        avatar_row.addStretch()

        edit_row = QHBoxLayout()
        edit_row.setContentsMargins(0, 6, 0, 8)
        edit_row.addStretch()
        edit_row.addWidget(self.edit_profile_button)

        bio_box = QFrame()
        bio_box.setObjectName("profileBioBox")
        bio_box_layout = QVBoxLayout(bio_box)
        bio_box_layout.setContentsMargins(22, 18, 22, 22)
        bio_box_layout.setSpacing(14)
        bio_box_layout.addWidget(self.bio_title_label)
        bio_box_layout.addWidget(self.bio_label, 1)

        content_layout.addWidget(self.title_label)
        content_layout.addLayout(avatar_row)
        content_layout.addWidget(self.email_label)
        content_layout.addWidget(self.username_label)
        content_layout.addLayout(edit_row)
        content_layout.addWidget(bio_box, 1)

        outer_layout.addWidget(self.content_frame)
        self.setLayout(outer_layout)

    def connect_signals(self):
        self.edit_profile_button.clicked.connect(self.open_edit_profile_dialog)

    def load_user_data(self):
        response = get_me()

        if response is None or response.status_code != 200:
            self.email_label.setText("brak danych")
            self.username_label.setText("brak danych")
            self.bio_label.setText("brak danych")
            self.avatar_label.setText("Brak avatara")
            return

        self.user_data = response.json()

        email = self.user_data.get("email", "brak danych")
        username = self.user_data.get("userName", "brak danych")
        bio = self.user_data.get("bio", "brak danych")
        avatar_url = self.user_data.get("avatarUrl")

        self.email_label.setText(email)
        self.username_label.setText(username)
        self.bio_label.setText(bio or "brak danych")

        self.load_avatar(avatar_url)

    def load_avatar(self, avatar_url):
        if not avatar_url:
            self.avatar_label.setText("Brak avatara")
            self.avatar_label.setPixmap(QPixmap())
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
                self.avatar_label.setPixmap(QPixmap())
                return

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            if pixmap.isNull():
                self.avatar_label.setText("Brak avatara")
                self.avatar_label.setPixmap(QPixmap())
                return

            self.avatar_label.setText("")
            self.avatar_label.setPixmap(self.create_round_avatar(pixmap, 150))
        except requests.RequestException:
            self.avatar_label.setText("Brak avatara")
            self.avatar_label.setPixmap(QPixmap())

    def create_round_avatar(self, pixmap, size):
        scaled = pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        x = max(0, (scaled.width() - size) // 2)
        y = max(0, (scaled.height() - size) // 2)
        cropped = scaled.copy(QRect(x, y, size, size))

        rounded = QPixmap(size, size)
        rounded.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, cropped)
        painter.end()

        return rounded

    def open_edit_profile_dialog(self):
        username = self.user_data.get("userName", "")
        bio = self.user_data.get("bio", "")

        dialog = EditProfileDialog(username, bio)
        result = dialog.exec()

        if result != EditProfileDialog.DialogCode.Accepted:
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
