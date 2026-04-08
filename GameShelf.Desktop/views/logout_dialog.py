from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class LogoutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Confirm Logout")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("Are you sure you want to log out?")
        label.setWordWrap(True)

        buttons_layout = QHBoxLayout()

        self.logout_button = QPushButton("Logout")
        self.cancel_button = QPushButton("Cancel")

        buttons_layout.addWidget(self.logout_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addWidget(label)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.logout_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)