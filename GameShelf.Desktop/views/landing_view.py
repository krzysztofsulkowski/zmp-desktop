from pathlib import Path

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QFontDatabase
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QSizePolicy
)


from utils.window_corners import disable_windows_11_rounded_corners

class LandingView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.setObjectName("LandingView")

        self.controller = controller
        self.drag_position = QPoint()
        self.is_dragging = False
        self.base_dir = Path(__file__).resolve().parents[1]

        self.load_fonts()
        self.setWindowTitle("GameShelf")
        self.setMinimumSize(1200, 720)
        self.resize(1440, 840)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setup_ui()
        self.connect_signals()

    def showEvent(self, event):
        super().showEvent(event)
        disable_windows_11_rounded_corners(self)

    def load_fonts(self):
        font_dir = self.base_dir / "assets"
        for font_path in font_dir.glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(font_path))
        for font_path in font_dir.glob("*.otf"):
            QFontDatabase.addApplicationFont(str(font_path))

    def setup_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.main_frame = QFrame()
        self.main_frame.setObjectName("landingFrame")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 24, 28, 40)
        main_layout.setSpacing(0)

        main_layout.addLayout(self.create_window_controls_bar())
        main_layout.addSpacing(12)
        main_layout.addLayout(self.create_navigation_bar())
        main_layout.addSpacing(36)
        main_layout.addLayout(self.create_content_layout())

        self.main_frame.setLayout(main_layout)
        outer_layout.addWidget(self.main_frame)
        self.setLayout(outer_layout)

    def create_window_controls_bar(self):
        controls_bar = QHBoxLayout()
        controls_bar.setContentsMargins(0, 0, 12, 0)
        controls_bar.setSpacing(10)

        self.minimize_button = QPushButton("—")
        self.maximize_button = QPushButton("□")
        self.close_button = QPushButton("×")

        self.minimize_button.setObjectName("windowControlButton")
        self.maximize_button.setObjectName("windowControlButton")
        self.close_button.setObjectName("windowCloseButton")

        for button in [self.minimize_button, self.maximize_button, self.close_button]:
            button.setFixedSize(34, 34)

        controls_bar.addStretch()
        controls_bar.addWidget(self.minimize_button)
        controls_bar.addWidget(self.maximize_button)
        controls_bar.addWidget(self.close_button)

        return controls_bar

    def create_navigation_bar(self):
        navigation_bar = QHBoxLayout()
        navigation_bar.setContentsMargins(0, 0, 132, 0)
        navigation_bar.setSpacing(18)

        self.login_button = QPushButton("LOGOWANIE")
        self.login_button.setObjectName("landingLoginButton")
        self.login_button.setFixedSize(132, 42)

        self.register_button = QPushButton("REJESTRACJA")
        self.register_button.setObjectName("landingRegisterButton")
        self.register_button.setFixedSize(176, 46)

        navigation_bar.addStretch()
        navigation_bar.addWidget(self.login_button)
        navigation_bar.addWidget(self.register_button)

        return navigation_bar

    def create_content_layout(self):
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(18, 10, -118, 0)
        content_layout.setSpacing(28)

        left_side = self.create_left_section()
        right_side = self.create_right_section()

        content_layout.addLayout(left_side, 5)
        content_layout.addLayout(right_side, 7)

        return content_layout

    def create_left_section(self):
        left_side = QVBoxLayout()
        left_side.setContentsMargins(0, 0, 0, 78)
        left_side.setSpacing(18)
        left_side.setAlignment(Qt.AlignVCenter)

        self.logo_label = QLabel()
        self.logo_label.setObjectName("landingLogo")
        self.logo_label.setFixedSize(220, 116)
        self.logo_label.setAlignment(Qt.AlignCenter)

        logo_path = self.base_dir / "assets" / "logo.svg"
        logo_pixmap = QPixmap(str(logo_path))

        if logo_pixmap.isNull():
            self.logo_label.setText("GameShelf")
        else:
            self.logo_label.setPixmap(
                logo_pixmap.scaled(
                    200,
                    106,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        self.headline_label = QLabel(
            "Twoje gry w jednym miejscu. I ludzie,\nktórzy grają w to samo."
        )
        self.headline_label.setObjectName("landingHeadline")
        self.headline_label.setAlignment(Qt.AlignCenter)
        self.headline_label.setWordWrap(True)
        self.headline_label.setFixedWidth(620)

        self.description_label = QLabel(
            "Uporządkuj gry z różnych platform i sprawdzaj, w co grają Twoi\n"
            "znajomi - w jednym miejscu, bez przełączania między aplikacjami."
        )
        self.description_label.setObjectName("landingDescription")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_label.setFixedWidth(560)

        self.join_button = QPushButton("DOŁĄCZ DO NAS!")
        self.join_button.setObjectName("landingJoinButton")
        self.join_button.setFixedSize(236, 48)

        self.small_text_label = QLabel("Zarejestruj się za darmo i rozpocznij tworzenie kolekcji!")
        self.small_text_label.setObjectName("landingSmallText")
        self.small_text_label.setAlignment(Qt.AlignCenter)

        left_side.addStretch()
        left_side.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        left_side.addSpacing(22)
        left_side.addWidget(self.headline_label, alignment=Qt.AlignCenter)
        left_side.addWidget(self.description_label, alignment=Qt.AlignCenter)
        left_side.addSpacing(18)
        left_side.addWidget(self.join_button, alignment=Qt.AlignCenter)
        left_side.addWidget(self.small_text_label, alignment=Qt.AlignCenter)
        left_side.addStretch()

        return left_side

    def create_right_section(self):
        right_side = QVBoxLayout()
        right_side.setContentsMargins(0, 0, 0, 46)
        right_side.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        self.offer_label = QLabel()
        self.offer_label.setObjectName("landingOfferImage")
        self.offer_label.setMinimumSize(760, 360)
        self.offer_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.offer_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        offer_path = self.base_dir / "assets" / "offer.png"
        offer_pixmap = QPixmap(str(offer_path))

        if offer_pixmap.isNull():
            self.offer_label.setText("")
        else:
            self.offer_label.setPixmap(
                offer_pixmap.scaled(
                    780,
                    360,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        right_side.addWidget(self.offer_label, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return right_side

    def connect_signals(self):
        self.login_button.clicked.connect(self.controller.show_login)
        self.register_button.clicked.connect(self.controller.show_register)
        self.join_button.clicked.connect(self.controller.show_register)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.close_button.clicked.connect(self.close)

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() <= 90:
            self.is_dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() == Qt.LeftButton and not self.isMaximized():
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        event.accept()
