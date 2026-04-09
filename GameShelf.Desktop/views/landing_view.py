from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt


class LandingView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.setWindowTitle("GameShelf")
        self.setMinimumSize(1440, 840)

        self.load_stylesheet()
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(30, 30, 30, 30)

        self.main_frame = QFrame()
        self.main_frame.setObjectName("landingFrame")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(45, 35, 45, 35)
        main_layout.setSpacing(0)

        top_bar = self.create_top_bar()
        content_layout = self.create_content_layout()

        main_layout.addLayout(top_bar)
        main_layout.addLayout(content_layout)

        self.main_frame.setLayout(main_layout)
        outer_layout.addWidget(self.main_frame)

        self.setLayout(outer_layout)

    def create_top_bar(self):
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.addStretch()

        self.login_button = QPushButton("LOGOWANIE")
        self.login_button.setFixedSize(150, 45)

        self.register_button = QPushButton("REJESTRACJA")
        self.register_button.setFixedSize(175, 47)
        self.register_button.setObjectName("primaryButton")

        top_bar.addWidget(self.login_button)
        top_bar.addSpacing(20)
        top_bar.addWidget(self.register_button)

        return top_bar

    def create_content_layout(self):
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 40, 0, 0)
        content_layout.setSpacing(70)

        left_side = self.create_left_section()
        right_side = self.create_right_section()

        content_layout.addLayout(left_side, 1)
        content_layout.addLayout(right_side, 1)

        return content_layout

    def create_left_section(self):
        left_side = QVBoxLayout()
        left_side.setSpacing(18)
        left_side.setAlignment(Qt.AlignCenter)

        self.logo_label = QLabel("GAME SHELF LOGO")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setObjectName("landingLogo")
        self.logo_label.setFixedHeight(120)

        self.headline_label = QLabel(
            "Twoje gry w jednym miejscu. I ludzie,\nktórzy grają w to samo."
        )
        self.headline_label.setAlignment(Qt.AlignCenter)
        self.headline_label.setObjectName("landingHeadline")
        self.headline_label.setFixedWidth(584)

        self.description_label = QLabel(
            "Uporządkuj gry z różnych platform i sprawdzaj, w co grają Twoi\n"
            "znajomi - w jednym miejscu, bez przełączania między aplikacjami."
        )
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setObjectName("landingDescription")
        self.description_label.setFixedWidth(584)
        self.description_label.setWordWrap(True)

        self.join_button = QPushButton("DOŁĄCZ DO NAS!")
        self.join_button.setFixedSize(232, 40)
        self.join_button.setObjectName("primaryButton")

        self.small_text_label = QLabel(
            "Zarejestruj się za darmo i rozpocznij tworzenie kolekcji!"
        )
        self.small_text_label.setAlignment(Qt.AlignCenter)
        self.small_text_label.setObjectName("landingSmallText")

        left_side.addStretch()
        left_side.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        left_side.addSpacing(35)
        left_side.addWidget(self.headline_label, alignment=Qt.AlignCenter)
        left_side.addWidget(self.description_label, alignment=Qt.AlignCenter)
        left_side.addSpacing(18)
        left_side.addWidget(self.join_button, alignment=Qt.AlignCenter)
        left_side.addWidget(self.small_text_label, alignment=Qt.AlignCenter)
        left_side.addStretch()

        return left_side

    def create_right_section(self):
        right_side = QVBoxLayout()
        right_side.setAlignment(Qt.AlignCenter)

        self.preview_placeholder = QFrame()
        self.preview_placeholder.setObjectName("previewPlaceholder")
        self.preview_placeholder.setFixedSize(722, 384)

        right_side.addStretch()
        right_side.addWidget(self.preview_placeholder, alignment=Qt.AlignCenter)
        right_side.addStretch()

        return right_side

    def connect_signals(self):
        self.login_button.clicked.connect(self.controller.show_login)
        self.register_button.clicked.connect(self.controller.show_register)
        self.join_button.clicked.connect(self.controller.show_register)

    def load_stylesheet(self):
        with open("GameShelf.Desktop/styles/landing_view.qss", "r") as file:
            self.setStyleSheet(file.read())