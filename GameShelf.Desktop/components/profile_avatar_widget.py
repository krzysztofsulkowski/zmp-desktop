from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

from services.avatar_service import load_round_avatar


class ProfileAvatarWidget(QLabel):
    def __init__(self, size=150):
        super().__init__("Brak avatara")
        self.avatar_size = size
        self.setObjectName("profileAvatar")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(size, size)

    def set_avatar_url(self, avatar_url):
        pixmap = load_round_avatar(avatar_url, self.avatar_size)

        if pixmap.isNull():
            self.clear_avatar()
            return

        self.setText("")
        self.setPixmap(pixmap)

    def clear_avatar(self):
        self.setText("Brak avatara")
        self.setPixmap(QPixmap())
