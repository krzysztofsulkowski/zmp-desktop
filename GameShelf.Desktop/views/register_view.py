from pathlib import Path

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QIcon, QFontDatabase
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame

from utils.window_corners import disable_windows_11_rounded_corners

from services.auth_service import register
from views.styled_dialog import show_info, show_warning


class RegisterView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.drag_position = QPoint()
        self.is_dragging = False
        self.base_dir = Path(__file__).resolve().parents[1]

        self.load_fonts()
        self.setWindowTitle("Rejestracja")
        self.setObjectName("authPage")
        self.setMinimumSize(940, 620)
        self.resize(980, 660)
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
        self.main_frame.setObjectName("authFrame")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(34, 24, 34, 40)
        main_layout.setSpacing(0)

        main_layout.addLayout(self.create_window_controls_bar())
        main_layout.addStretch()
        main_layout.addWidget(self.create_logo(), alignment=Qt.AlignCenter)
        main_layout.addSpacing(18)
        main_layout.addWidget(self.create_card(), alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.main_frame.setLayout(main_layout)
        outer_layout.addWidget(self.main_frame)
        self.setLayout(outer_layout)

    def create_window_controls_bar(self):
        controls_bar = QHBoxLayout()
        controls_bar.setContentsMargins(0, 0, 6, 0)
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

    def create_logo(self):
        self.logo_label = QLabel()
        self.logo_label.setObjectName("authTopLogo")
        self.logo_label.setFixedSize(150, 78)
        self.logo_label.setAlignment(Qt.AlignCenter)

        logo_path = self.base_dir / "assets" / "logo.svg"
        logo_pixmap = QPixmap(str(logo_path))

        if logo_pixmap.isNull():
            self.logo_label.setText("GameShelf")
        else:
            self.logo_label.setPixmap(
                logo_pixmap.scaled(
                    140,
                    72,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        return self.logo_label

    def create_card(self):
        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedSize(360, 455)

        layout = QVBoxLayout()
        layout.setContentsMargins(44, 28, 44, 30)
        layout.setSpacing(6)

        self.title = QLabel("Rejestracja")
        self.title.setObjectName("authTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.email_input = self.create_input("adres e-mail")
        self.username_input = self.create_input("nazwa użytkownika")
        self.password_input = self.create_input("hasło")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.repeat_password_input = self.create_input("powtórz hasło")
        self.repeat_password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Zarejestruj się")
        self.register_button.setObjectName("authPrimaryButton")
        self.register_button.setFixedHeight(34)

        self.or_label = QLabel("lub")
        self.or_label.setObjectName("authOrLabel")
        self.or_label.setAlignment(Qt.AlignCenter)

        self.google_button = QPushButton("Kontynuuj przez Google")
        self.google_button.setObjectName("authSecondaryButton")
        self.google_button.setFixedHeight(34)

        google_icon_path = self.base_dir / "assets" / "google.svg"

        if google_icon_path.exists():
            self.google_button.setIcon(QIcon(str(google_icon_path)))

        self.login_link = QLabel('Masz już konto? <a href="login">Zaloguj się</a>')
        self.login_link.setObjectName("authLoginLink")
        self.login_link.setAlignment(Qt.AlignCenter)
        self.login_link.setTextFormat(Qt.RichText)
        self.login_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.login_link.setOpenExternalLinks(False)

        layout.addWidget(self.title)
        layout.addSpacing(10)
        layout.addWidget(self.create_field("adres e-mail", self.email_input))
        layout.addWidget(self.create_field("nazwa użytkownika", self.username_input))
        layout.addWidget(self.create_field("hasło", self.password_input))
        layout.addWidget(self.create_field("powtórz hasło", self.repeat_password_input))
        layout.addSpacing(6)
        layout.addWidget(self.register_button)
        layout.addWidget(self.or_label)
        layout.addWidget(self.google_button)
        layout.addSpacing(6)
        layout.addWidget(self.login_link)

        card.setLayout(layout)

        return card

    def create_field(self, label_text, input_widget):
        field = QWidget()
        field.setObjectName("authFieldWrapper")
        field.setFixedHeight(57)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel(label_text)
        label.setObjectName("authInputLabel")

        layout.addWidget(label)
        layout.addWidget(input_widget)

        field.setLayout(layout)

        return field

    def create_input(self, placeholder):
        input_widget = QLineEdit()
        input_widget.setPlaceholderText(placeholder)
        input_widget.setMinimumHeight(31)
        input_widget.setFixedHeight(31)
        input_widget.setObjectName("authInput")

        return input_widget

    def connect_signals(self):
        self.register_button.clicked.connect(self.handle_register)
        self.login_link.linkActivated.connect(self.controller.show_login)
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

    def handle_register(self):
        email = self.email_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()

        if not email or not username or not password or not repeat_password:
            show_warning(self, "Wszystkie pola są wymagane.")
            return

        if password != repeat_password:
            show_warning(self, "Hasła nie są takie same.")
            return

        success, error = register(email, username, password)

        if success:
            show_info(self, "Konto zostało utworzone.")
            self.controller.show_login()
        else:
            show_warning(self, error)