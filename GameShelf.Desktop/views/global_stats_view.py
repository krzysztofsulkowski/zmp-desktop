from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt

from services.statistics_service import get_global_statistics


class GlobalStatsCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("globalStatsCard")
        self.setFixedSize(320, 320)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 18, 20, 18)
        self.layout.setSpacing(14)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("globalStatsCardTitle")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.title_label)


class GlobalStatsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("globalStatsView")

        self.cards = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(32, 28, 32, 28)
        self.main_layout.setSpacing(24)

        self.title_label = QLabel("Globalne statystyki")
        self.title_label.setObjectName("globalStatsPageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("globalStatsScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("globalStatsScrollWidget")

        self.grid = QGridLayout(self.scroll_widget)
        self.grid.setContentsMargins(0, 0, 0, 24)
        self.grid.setHorizontalSpacing(14)
        self.grid.setVerticalSpacing(26)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.total_users_card = self.create_number_card("liczba użytkowników:")
        self.total_library_games_card = self.create_number_card("liczba gier w bibliotece globalnej:")
        self.total_user_games_card = self.create_number_card("liczba gier w kolekcjach użytkowników:")

        self.popular_games_card = self.create_list_card("najpopularniejsze gry:")
        self.popular_platforms_card = self.create_list_card("najpopularniejsze platformy:")
        self.popular_genres_card = self.create_list_card("najpopularniejsze gatunki:")
        self.highest_rated_games_card = self.create_list_card("najwyżej oceniane gry:")

        self.cards = [
            self.total_users_card,
            self.total_library_games_card,
            self.total_user_games_card,
            self.popular_games_card,
            self.popular_platforms_card,
            self.popular_genres_card,
            self.highest_rated_games_card
        ]

        self.rebuild_grid(3)
        self.load_statistics()

    def create_number_card(self, title):
        card = GlobalStatsCard(title)

        value_label = QLabel("0")
        value_label.setObjectName("globalStatsNumber")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card.layout.addStretch(1)
        card.layout.addWidget(value_label)
        card.layout.addStretch(1)

        card.value_label = value_label

        return card

    def create_list_card(self, title):
        card = GlobalStatsCard(title)

        list_container = QVBoxLayout()
        list_container.setContentsMargins(0, 8, 0, 0)
        list_container.setSpacing(10)

        card.layout.addLayout(list_container)
        card.layout.addStretch(1)

        card.items_layout = list_container

        return card

    def clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()

            if widget:
                widget.setParent(None)

    def rebuild_grid(self, columns):
        self.clear_grid()

        for index, card in enumerate(self.cards):
            row = index // columns
            column = index % columns
            self.grid.addWidget(card, row, column, Qt.AlignmentFlag.AlignCenter)

    def update_grid_columns(self):
        card_width = 320
        gap = 14

        viewport_width = self.scroll_area.viewport().width()
        window_width = self.window().width() - 210 if self.window() else 0
        available_width = max(viewport_width, window_width)

        columns = max(1, min(3, (available_width + gap) // (card_width + gap)))

        if available_width >= 1000:
            columns = 3
        elif available_width >= 660:
            columns = 2
        else:
            columns = 1

        self.rebuild_grid(columns)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grid_columns()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_grid_columns()

    def load_statistics(self):
        stats = get_global_statistics()

        if not stats:
            self.total_users_card.value_label.setText("—")
            self.total_library_games_card.value_label.setText("—")
            self.total_user_games_card.value_label.setText("—")
            self.fill_list_card(self.popular_games_card, [])
            self.fill_list_card(self.popular_platforms_card, [])
            self.fill_list_card(self.popular_genres_card, [])
            self.fill_list_card(self.highest_rated_games_card, [])
            return

        self.total_users_card.value_label.setText(str(stats.get("totalUsers", 0)))
        self.total_library_games_card.value_label.setText(str(stats.get("totalGamesInLibrary", 0)))
        self.total_user_games_card.value_label.setText(str(stats.get("totalUserGames", 0)))

        self.fill_list_card(self.popular_games_card, stats.get("mostPopularGames", []))
        self.fill_list_card(self.popular_platforms_card, stats.get("popularPlatforms", []))
        self.fill_list_card(self.popular_genres_card, stats.get("popularGenres", []))
        self.fill_list_card(self.highest_rated_games_card, stats.get("highestRatedGames", []))

    def fill_list_card(self, card, items):
        while card.items_layout.count():
            item = card.items_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not items:
            empty_label = QLabel("Brak danych")
            empty_label.setObjectName("globalStatsListItem")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card.items_layout.addWidget(empty_label)
            return

        for item in items[:6]:
            label = item.get("label", "Brak")
            value = item.get("value", 0)

            item_label = QLabel(f"{label}: {value}")
            item_label.setObjectName("globalStatsListItem")
            item_label.setWordWrap(True)
            item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card.items_layout.addWidget(item_label)
