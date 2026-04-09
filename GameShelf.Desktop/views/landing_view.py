from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PySide6.QtCore import Qt


class LandingView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.setWindowTitle("GameShelf")

        main_layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        top_bar.addWidget(self.login_button)
        top_bar.addWidget(self.register_button)

        content_layout = QHBoxLayout()

        left_side = QVBoxLayout()
        right_side = QVBoxLayout()

        self.logo_label = QLabel("GAME SHELF LOGO")
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.headline_label = QLabel(
            "Twoje gry w jednym miejscu. I ludzie,\nktórzy grają w to samo."
        )
        self.headline_label.setAlignment(Qt.AlignCenter)

        self.description_label = QLabel(
            "Uporządkuj gry z różnych platform i sprawdzaj, w co grają Twoi\n"
            "znajomi - w jednym miejscu, bez przełączania między aplikacjami."
        )
        self.description_label.setAlignment(Qt.AlignCenter)

        self.join_button = QPushButton("DOŁĄCZ DO NAS!")

        self.small_text_label = QLabel(
            "Zarejestruj się za darmo i rozpocznij tworzenie kolekcji!"
        )
        self.small_text_label.setAlignment(Qt.AlignCenter)

        left_side.addStretch()
        left_side.addWidget(self.logo_label)
        left_side.addSpacing(20)
        left_side.addWidget(self.headline_label)
        left_side.addSpacing(15)
        left_side.addWidget(self.description_label)
        left_side.addSpacing(20)
        left_side.addWidget(self.join_button)
        left_side.addSpacing(10)
        left_side.addWidget(self.small_text_label)
        left_side.addStretch()

        self.preview_placeholder = QLabel("PREVIEW IMAGE PLACEHOLDER")
        self.preview_placeholder.setAlignment(Qt.AlignCenter)

        right_side.addStretch()
        right_side.addWidget(self.preview_placeholder)
        right_side.addStretch()

        content_layout.addLayout(left_side, 1)
        content_layout.addLayout(right_side, 1)

        main_layout.addLayout(top_bar)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        self.login_button.clicked.connect(self.controller.show_login)
        self.register_button.clicked.connect(self.controller.show_register)
        self.join_button.clicked.connect(self.controller.show_register)