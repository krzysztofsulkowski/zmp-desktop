from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel
)
from PySide6.QtCore import Qt


class ForgotPasswordView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Forgot Password")

        main_layout = QVBoxLayout()

        self.back_button = QPushButton("←")
        self.back_button.setFixedWidth(40)

        self.title_label = QLabel("Zresetuj hasło")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("adres e-mail")

        self.info_label = QLabel(
            "Na Twój adres e-mail wyślemy link, który umożliwi Ci zmianę hasła."
        )
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignCenter)

        self.send_button = QPushButton("Wyślij link")

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.title_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.info_label)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.send_button)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.back_button.clicked.connect(self.controller.show_login)
        self.send_button.clicked.connect(self.handle_send_link)

    def handle_send_link(self):
        email = self.email_input.text().strip()

        if not email:
            self.status_label.setText("Podaj adres e-mail.")
            return

        self.status_label.setText("to be added")