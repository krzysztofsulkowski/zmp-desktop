from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox
)


class EditProfileDialog(QDialog):
    def __init__(self, username, bio):
        super().__init__()

        self.avatar_path = None

        self.setWindowTitle("Edytuj profil")
        self.setMinimumWidth(500)

        self.username_input = QLineEdit(username)
        self.bio_input = QTextEdit()
        self.bio_input.setPlainText(bio or "")

        self.avatar_label = QLabel("Nie wybrano pliku")
        self.avatar_button = QPushButton("Wybierz avatar")
        self.save_button = QPushButton("Zapisz zmiany")

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nazwa użytkownika"))
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Bio"))
        layout.addWidget(self.bio_input)

        layout.addWidget(QLabel("Avatar"))
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.avatar_button)

        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def connect_signals(self):
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
        self.avatar_label.setText(file_path)

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