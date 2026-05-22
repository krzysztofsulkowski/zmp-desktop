from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy
)

from components.profile_avatar_widget import ProfileAvatarWidget
from services.user_service import get_current_user
from services.profile_service import update_profile
from views.edit_profile_dialog import EditProfileDialog
from views.styled_dialog import show_info, show_warning


class ProfileView(QWidget):
    def __init__(self, on_logout):
        super().__init__()
        self.setObjectName("profileView")

        self.on_logout = on_logout
        self.user_data = {}

        self.title_label = QLabel("Profil użytkownika")
        self.title_label.setObjectName("profilePageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.avatar_label = ProfileAvatarWidget(150)

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
        self.user_data = get_current_user()

        if not self.user_data:
            self.email_label.setText("brak danych")
            self.username_label.setText("brak danych")
            self.bio_label.setText("brak danych")
            self.avatar_label.clear_avatar()
            return

        self.email_label.setText(self.user_data.get("email", "brak danych"))
        self.username_label.setText(self.user_data.get("userName", "brak danych"))
        self.bio_label.setText(self.user_data.get("bio") or "brak danych")
        self.avatar_label.set_avatar_url(self.user_data.get("avatarUrl"))

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
            show_warning(self, f"Nie udało się zaktualizować profilu.\n\n{error}")
            return

        show_info(self, "Profil został zaktualizowany.")

        self.load_user_data()
