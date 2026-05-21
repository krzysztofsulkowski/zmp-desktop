from pathlib import Path

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame
)


class EditProfileDialog(QDialog):
    def __init__(self, username, bio):
        super().__init__()

        self.avatar_path = None
        self.drag_position = QPoint()
        self.is_dragging = False

        self.setObjectName("editProfileDialog")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)
        self.setMinimumWidth(520)

        self.title_label = QLabel("Edytuj profil")
        self.title_label.setObjectName("editProfileDialogTitle")

        self.close_button = QPushButton("×")
        self.close_button.setObjectName("editProfileCloseButton")
        self.close_button.setFixedSize(36, 36)

        self.username_input = QLineEdit(username)
        self.username_input.setObjectName("editProfileInput")

        self.bio_input = QTextEdit()
        self.bio_input.setObjectName("editProfileTextArea")
        self.bio_input.setPlainText(bio or "")
        self.bio_input.setFixedHeight(150)

        self.avatar_label = QLabel("Nie wybrano pliku")
        self.avatar_label.setObjectName("editProfileFileLabel")
        self.avatar_label.setWordWrap(True)

        self.avatar_button = QPushButton("Wybierz avatar")
        self.avatar_button.setObjectName("editProfileSecondaryButton")

        self.save_button = QPushButton("Zapisz zmiany")
        self.save_button.setObjectName("editProfilePrimaryButton")

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame()
        self.frame.setObjectName("editProfileDialogFrame")

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(22, 18, 22, 22)
        layout.setSpacing(12)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 8)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_button)

        layout.addLayout(header_layout)
        layout.addWidget(QLabel("Nazwa użytkownika"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Bio"))
        layout.addWidget(self.bio_input)
        layout.addWidget(QLabel("Avatar"))
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.avatar_button)
        layout.addWidget(self.save_button)

        outer_layout.addWidget(self.frame)

    def connect_signals(self):
        self.close_button.clicked.connect(self.reject)
        self.avatar_button.clicked.connect(self.select_avatar)
        self.save_button.clicked.connect(self.validate_and_accept)

    def select_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz avatar",
            "",
            "Obrazy (*.png *.jpg *.jpeg *.webp)"
        )

        if not file_path:
            return

        self.avatar_path = file_path
        self.avatar_label.setText(Path(file_path).name)

    def validate_and_accept(self):
        if not self.get_username():
            QMessageBox.warning(
                self,
                "GameShelf",
                "Nazwa użytkownika jest wymagana."
            )
            return

        self.accept()

    def get_username(self):
        return self.username_input.text().strip()

    def get_bio(self):
        return self.bio_input.toPlainText().strip()

    def get_avatar_path(self):
        return self.avatar_path

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        event.accept()
