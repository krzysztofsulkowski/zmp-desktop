from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QGridLayout, QStackedLayout
)
from services.collection_service import get_my_collection
from views.friends_view import FriendsView


class MainView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GameShelf")

        self.current_filter = "all"

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

        self.tabs_layout = QHBoxLayout()

        self.tab_all = QPushButton("Biblioteka")
        self.tab_fav = QPushButton("Ulubione")
        self.tab_planned = QPushButton("Planowane")
        self.tab_wishlist = QPushButton("Lista życzeń")

        self.tabs_layout.addWidget(self.tab_all)
        self.tabs_layout.addWidget(self.tab_fav)
        self.tabs_layout.addWidget(self.tab_planned)
        self.tabs_layout.addWidget(self.tab_wishlist)
        self.tabs_layout.addStretch()

        self.tab_all.clicked.connect(lambda: self.change_tab("all"))
        self.tab_fav.clicked.connect(lambda: self.change_tab("fav"))
        self.tab_planned.clicked.connect(lambda: self.change_tab("planned"))
        self.tab_wishlist.clicked.connect(lambda: self.change_tab("wishlist"))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout()

        self.scroll_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.stacked_layout = QStackedLayout()

        self.home_widget = QWidget()
        home_layout = QVBoxLayout()

        home_layout.addLayout(self.tabs_layout)
        home_layout.addWidget(self.scroll_area)

        self.home_widget.setLayout(home_layout)

        self.friends_view = FriendsView()

        self.stacked_layout.addWidget(self.home_widget)
        self.stacked_layout.addWidget(self.friends_view)

        content_layout.addLayout(self.stacked_layout)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(content_layout, 4)

        self.setLayout(main_layout)

        self.home_button.clicked.connect(lambda: self.switch_view(0))
        self.friends_button.clicked.connect(lambda: self.switch_view(1))

        self.load_games()

    def switch_view(self, index):
        self.stacked_layout.setCurrentIndex(index)

    def change_tab(self, tab):
        self.current_filter = tab
        self.load_games()

    def load_games(self):
        games = get_my_collection()

        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        row = 0
        col = 0

        for game in games:
            card = self.create_game_card(game)

            self.grid_layout.addWidget(card, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1

    def create_game_card(self, game):
        card = QWidget()
        layout = QVBoxLayout()

        title = QLabel(game.title if hasattr(game, "title") else str(game))
        title.setStyleSheet("font-weight: bold;")

        genre = QLabel(game.genre if hasattr(game, "genre") else "")

        layout.addWidget(title)
        layout.addWidget(genre)

        card.setLayout(layout)

        card.setFixedSize(200, 120)

        card.setStyleSheet("""
            QWidget {
                background-color: #2a2a3d;
                border-radius: 10px;
                padding: 8px;
                color: white;
            }
        """)

        return card