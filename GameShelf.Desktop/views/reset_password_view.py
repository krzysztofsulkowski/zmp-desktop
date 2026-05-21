from pathlib import Path

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QFontDatabase
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFrame

from utils.window_corners import disable_windows_11_rounded_corners

from services.auth_service import reset_password


class ResetPasswordView(QWidget):
    def __init__(self, on_back_to_login):
        super().__init__()

        self.on_back_to_login = on_back_to_login
        self.drag_position = QPoint()
        self.is_dragging = False
        self.base_dir = Path(__file__).resolve().parents[1]

        self.load_fonts()
        self.setWindowTitle("Ustaw nowe hasło")
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
        card.setFixedSize(360, 430)

        layout = QVBoxLayout()
        layout.setContentsMargins(44, 28, 44, 30)
        layout.setSpacing(6)

        self.title_label = QLabel("Ustaw nowe hasło")
        self.title_label.setObjectName("authTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.email_input = self.create_input("adres e-mail")
        self.token_input = self.create_input("token resetujący")
        self.password_input = self.create_input("nowe hasło")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.info_label = QLabel("Wpisz adres e-mail, token resetujący oraz nowe hasło.")
        self.info_label.setObjectName("authInfoLabel")
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignCenter)

        self.reset_button = QPushButton("Ustaw nowe hasło")
        self.reset_button.setObjectName("authPrimaryButton")
        self.reset_button.setFixedHeight(34)

        self.back_button = QPushButton("Powrót do logowania")
        self.back_button.setObjectName("authSecondaryButton")
        self.back_button.setFixedHeight(34)

        layout.addStretch()
        layout.addWidget(self.title_label)
        layout.addSpacing(18)
        layout.addWidget(self.create_field("adres e-mail", self.email_input))
        layout.addWidget(self.create_field("token resetujący", self.token_input))
        layout.addWidget(self.create_field("nowe hasło", self.password_input))
        layout.addWidget(self.info_label)
        layout.addSpacing(10)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.back_button)
        layout.addStretch()

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
        self.reset_button.clicked.connect(self.handle_reset_password)
        self.back_button.clicked.connect(self.on_back_to_login)
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

    def handle_reset_password(self):
        email = self.email_input.text().strip()
        token = self.token_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not token or not password:
            QMessageBox.warning(self, "GameShelf", "Wszystkie pola są wymagane.")
            return

        success, error = reset_password(email, token, password)

        if not success:
            QMessageBox.warning(self, "GameShelf", f"Nie udało się ustawić nowego hasła.\n\n{error}")
            return

        QMessageBox.information(self, "GameShelf", "Hasło zostało zmienione.")
        self.on_back_to_login()