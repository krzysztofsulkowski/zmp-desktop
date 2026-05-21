from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton

from views.styled_dialog import StyledDialog


class LogoutDialog(StyledDialog):
    def __init__(self):
        super().__init__("Wylogowanie")
        self.setFixedWidth(360)

        label = QLabel("Czy na pewno chcesz się wylogować?")
        label.setWordWrap(True)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.cancel_button = QPushButton("Anuluj")
        self.logout_button = QPushButton("Wyloguj")

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.logout_button)

        self.body_layout.addWidget(label)
        self.body_layout.addLayout(buttons_layout)

        self.logout_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
