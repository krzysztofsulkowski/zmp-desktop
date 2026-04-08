from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget
from services.collection_service import get_my_collection


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

        self.games_list = QListWidget()
        content_layout.addWidget(self.games_list)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(content_layout, 4)

        self.setLayout(main_layout)

        self.load_games()

    def load_games(self):
        games = get_my_collection()

        self.games_list.clear()

        for game in games:
            self.games_list.addItem(str(game))