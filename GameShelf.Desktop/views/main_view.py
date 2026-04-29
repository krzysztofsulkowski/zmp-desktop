from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QGridLayout, QStackedLayout, QDialog
)

from services.collection_service import get_my_collection, get_collections_lookup
from services.session import clear_token
from services.auth_service import logout

from views.friends_view import FriendsView
from views.stats_view import StatsView
from views.settings_view import SettingsView
from views.global_stats_view import GlobalStatsView
from views.notifications_view import NotificationsView
from views.logout_dialog import LogoutDialog
from views.create_collection_dialog import CreateCollectionDialog

class MainView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("GameShelf")
        self.current_filter = "all"

        main_layout = QHBoxLayout()

        sidebar = QVBoxLayout()

        self.home_button = QPushButton("Home")
        self.stats_button = QPushButton("Stats")
        self.friends_button = QPushButton("Friends")
        self.global_stats_button = QPushButton("Global Stats")
        self.notifications_button = QPushButton("Notifications")
        self.settings_button = QPushButton("Settings")
        self.logout_button = QPushButton("Logout")

        sidebar.addWidget(self.home_button)
        sidebar.addWidget(self.stats_button)
        sidebar.addWidget(self.friends_button)
        sidebar.addWidget(self.global_stats_button)
        sidebar.addWidget(self.notifications_button)
        sidebar.addWidget(self.settings_button)

        sidebar.addStretch()
        sidebar.addWidget(self.logout_button)

        content_layout = QVBoxLayout()

        self.tabs_layout = QHBoxLayout()

        self.tab_all = QPushButton("Biblioteka")
        self.tab_all.clicked.connect(lambda: self.change_tab("all"))

        self.collection_buttons = []

        self.add_collection_button = QPushButton("+")
        self.add_collection_button.setFixedSize(32, 32)

        self.tabs_layout.addWidget(self.tab_all)

        self.load_collection_tabs()

        self.add_collection_button.clicked.connect(self.handle_add_collection)

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
        self.stats_view = StatsView()
        self.settings_view = SettingsView()
        self.global_stats_view = GlobalStatsView()
        self.notifications_view = NotificationsView()

        self.stacked_layout.addWidget(self.home_widget)           # 0
        self.stacked_layout.addWidget(self.friends_view)          # 1
        self.stacked_layout.addWidget(self.stats_view)            # 2
        self.stacked_layout.addWidget(self.settings_view)         # 3
        self.stacked_layout.addWidget(self.global_stats_view)     # 4
        self.stacked_layout.addWidget(self.notifications_view)    # 5

        content_layout.addLayout(self.stacked_layout)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(content_layout, 4)

        self.setLayout(main_layout)

        self.home_button.clicked.connect(lambda: self.switch_view_with_highlight(0, self.home_button))
        self.friends_button.clicked.connect(lambda: self.switch_view_with_highlight(1, self.friends_button))
        self.stats_button.clicked.connect(lambda: self.switch_view_with_highlight(2, self.stats_button))
        self.settings_button.clicked.connect(lambda: self.switch_view_with_highlight(3, self.settings_button))
        self.global_stats_button.clicked.connect(lambda: self.switch_view_with_highlight(4, self.global_stats_button))
        self.notifications_button.clicked.connect(lambda: self.switch_view_with_highlight(5, self.notifications_button))

        self.logout_button.clicked.connect(self.logout_view)

        self.load_games()

        self.set_active_button(self.home_button)

    def switch_view(self, index):
        self.stacked_layout.setCurrentIndex(index)

    def logout_view(self):
        dialog = LogoutDialog()
        result = dialog.exec()

        if result == QDialog.Accepted:
            logout()
            clear_token()

            self.controller.show_login()

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
        genre = QLabel(game.genre if hasattr(game, "genre") else "")

        card.setObjectName("gameCard")
        title.setObjectName("gameTitle")
        genre.setObjectName("gameGenre")

        layout.addWidget(title)
        layout.addWidget(genre)

        card.setLayout(layout)
        card.setFixedSize(200, 120)

        return card

    def set_active_button(self, active_button):
        buttons = [
            self.home_button,
            self.stats_button,
            self.friends_button,
            self.global_stats_button,
            self.notifications_button,
            self.settings_button
        ]

        for button in buttons:
            button.setProperty("active", False)
            button.style().unpolish(button)
            button.style().polish(button)

        active_button.setProperty("active", True)
        active_button.style().unpolish(active_button)
        active_button.style().polish(active_button)

    def switch_view_with_highlight(self, index, button):
        self.switch_view(index)
        self.set_active_button(button)

    def handle_add_collection(self):
        from services.collection_service import create_collection

        dialog = CreateCollectionDialog()
        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        name, is_public = dialog.get_collection_data()

        if not name:
            print("Collection name is required")
            return

        success = create_collection(name, is_public)

        print("CREATE COLLECTION RESULT:", success)

        if success:
            self.load_collection_tabs()
            self.load_games()

    def load_collection_tabs(self):
        for button in self.collection_buttons:
            self.tabs_layout.removeWidget(button)
            button.deleteLater()

        self.collection_buttons.clear()

        self.tabs_layout.removeWidget(self.add_collection_button)

        collections = get_collections_lookup()

        for collection in collections:
            button = QPushButton(collection.get("name", "Bez nazwy"))

            button.clicked.connect(
                lambda checked=False, collection_id=collection.get("id"): self.change_tab(collection_id)
            )

            self.collection_buttons.append(button)
            self.tabs_layout.addWidget(button)

        self.tabs_layout.addWidget(self.add_collection_button)