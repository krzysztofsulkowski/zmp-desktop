from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel


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

        center_layout = QVBoxLayout()

        self.title_label = QLabel("Welcome to GameShelf")
        self.join_button = QPushButton("Dołącz do nas")

        center_layout.addWidget(self.title_label)
        center_layout.addWidget(self.join_button)

        main_layout.addLayout(top_bar)
        main_layout.addStretch()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.login_button.clicked.connect(self.controller.show_login)
        self.register_button.clicked.connect(self.controller.show_register)
        self.join_button.clicked.connect(self.controller.show_register)