from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton


class MainView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GameShelf")

        main_layout = QHBoxLayout()

        sidebar = QVBoxLayout()

        self.home_button = QPushButton("Home")
        self.stats_button = QPushButton("Stats")
        self.friends_button = QPushButton("Friends")
        self.settings_button = QPushButton("Settings")

        sidebar.addWidget(self.home_button)
        sidebar.addWidget(self.stats_button)
        sidebar.addWidget(self.friends_button)
        sidebar.addWidget(self.settings_button)
        sidebar.addStretch()

        content_layout = QVBoxLayout()

        self.content_label = QLabel("Main content area")

        content_layout.addWidget(self.content_label)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(content_layout, 4)

        self.setLayout(main_layout)