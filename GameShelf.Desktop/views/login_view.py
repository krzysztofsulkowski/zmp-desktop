from pathlib import Path

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QIcon, QFontDatabase
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame

from services.auth_service import login
from services.session import set_token


class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.drag_position = QPoint()
        self.is_dragging = False
        self.base_dir = Path(__file__).resolve().parents[1]

        self.load_fonts()
        self.setWindowTitle("Logowanie")
        self.setObjectName("authPage")
        self.setMinimumSize(940, 620)
        self.resize(980, 660)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setup_ui()
        self.connect_signals()

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
        card.setFixedSize(360, 405)

        layout = QVBoxLayout()
        layout.setContentsMargins(44, 28, 44, 30)
        layout.setSpacing(6)

        self.title_label = QLabel("Logowanie")
        self.title_label.setObjectName("authTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.email_input = self.create_input("adres e-mail")
        self.password_input = self.create_input("hasło")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.forgot_password_button = QPushButton("Nie pamiętam hasła")
        self.forgot_password_button.setObjectName("authForgotButton")

        self.login_button = QPushButton("Zaloguj się")
        self.login_button.setObjectName("authPrimaryButton")
        self.login_button.setFixedHeight(34)

        self.or_label = QLabel("lub")
        self.or_label.setObjectName("authOrLabel")
        self.or_label.setAlignment(Qt.AlignCenter)

        self.google_login_button = QPushButton("Kontynuuj przez Google")
        self.google_login_button.setObjectName("authSecondaryButton")
        self.google_login_button.setFixedHeight(34)

        google_icon_path = self.base_dir / "assets" / "google.svg"

        if google_icon_path.exists():
            self.google_login_button.setIcon(QIcon(str(google_icon_path)))

        self.register_link = QLabel('Nie posiadasz konta? <a href="register">Zarejestruj się</a>')
        self.register_link.setObjectName("authRegisterLink")
        self.register_link.setAlignment(Qt.AlignCenter)
        self.register_link.setTextFormat(Qt.RichText)
        self.register_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.register_link.setOpenExternalLinks(False)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()

        layout.addWidget(self.title_label)
        layout.addSpacing(18)
        layout.addWidget(self.create_field("adres e-mail", self.email_input))
        layout.addWidget(self.create_field("hasło", self.password_input))
        layout.addWidget(self.forgot_password_button, alignment=Qt.AlignLeft)
        layout.addSpacing(6)
        layout.addWidget(self.login_button)
        layout.addWidget(self.or_label)
        layout.addWidget(self.google_login_button)
        layout.addSpacing(12)
        layout.addWidget(self.register_link)
        layout.addWidget(self.status_label)

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
        self.login_button.clicked.connect(self.handle_login)
        self.forgot_password_button.clicked.connect(self.controller.show_forgot_password)
        self.register_link.linkActivated.connect(self.controller.show_register)
        self.google_login_button.clicked.connect(self.handle_google_login)
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

    def set_status(self, text, success=False):
        self.status_label.setText(text)
        self.status_label.setObjectName("authStatusSuccess" if success else "authStatusError")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.show()

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        token = login(email, password)

        if not token:
            self.set_status("Nie udało się zalogować.")
            return

        set_token(token)
        self.set_status("Zalogowano pomyślnie.", True)
        self.controller.show_main()

    def handle_google_login(self):
        self.set_status("Logowanie przez Google nie jest jeszcze dostępne.")