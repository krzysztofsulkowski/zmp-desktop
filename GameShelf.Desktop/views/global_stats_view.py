from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea

from components.stats_widgets import (
    GlobalStatsCard,
    PodiumBar,
    build_global_pie_chart,
    create_global_pie_chart_view,
    create_podium_layout,
)
from services.statistics_service import get_global_statistics


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

        self.popular_games_card, self.popular_games_chart = self.create_chart_card("najpopularniejsze gry:")
        self.popular_platforms_card, self.popular_platforms_chart = self.create_chart_card("najpopularniejsze platformy:")
        self.popular_genres_card, self.popular_genres_chart = self.create_chart_card("najpopularniejsze gatunki:")
        self.highest_rated_games_card = self.create_podium_card("najwyżej oceniane gry:")

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

    def create_chart_card(self, title):
        card = GlobalStatsCard(title)
        chart, chart_view = create_global_pie_chart_view()
        card.layout.addWidget(chart_view)
        return card, chart

    def create_podium_card(self, title):
        card = GlobalStatsCard(title)
        podium_layout = create_podium_layout()
        card.layout.addLayout(podium_layout)
        card.podium_layout = podium_layout
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
        self.load_statistics()

    def load_statistics(self):
        stats = get_global_statistics()

        if not stats:
            self.total_users_card.value_label.setText("—")
            self.total_library_games_card.value_label.setText("—")
            self.total_user_games_card.value_label.setText("—")
            self.build_pie_chart(self.popular_games_chart, [])
            self.build_pie_chart(self.popular_platforms_chart, [])
            self.build_pie_chart(self.popular_genres_chart, [])
            self.build_podium([])
            return

        self.total_users_card.value_label.setText(str(stats.get("totalUsers", 0)))
        self.total_library_games_card.value_label.setText(str(stats.get("totalGamesInLibrary", 0)))
        self.total_user_games_card.value_label.setText(str(stats.get("totalUserGames", 0)))

        self.build_pie_chart(self.popular_games_chart, stats.get("mostPopularGames", []))
        self.build_pie_chart(self.popular_platforms_chart, stats.get("popularPlatforms", []))
        self.build_pie_chart(self.popular_genres_chart, stats.get("popularGenres", []))
        self.build_podium(stats.get("highestRatedGames", []))

    def build_pie_chart(self, chart, items):
        build_global_pie_chart(chart, items, self)

    def clear_podium(self):
        while self.highest_rated_games_card.podium_layout.count():
            item = self.highest_rated_games_card.podium_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

    def build_podium(self, items):
        self.clear_podium()

        podium_items = items

        if not podium_items:
            empty_label = QLabel("Brak danych")
            empty_label.setObjectName("globalStatsListItem")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.highest_rated_games_card.podium_layout.addWidget(empty_label)
            return

        sorted_items = sorted(
            podium_items,
            key=lambda item: item.get("value", 0),
            reverse=True
        )

        colors_by_place = ["#D6B35A", "#BFB7D6", "#B8734A"]
        heights_by_place = [132, 104, 82]

        for item in sorted_items:
            name = item.get("label", "Brak")
            value = item.get("value", 0)

            same_or_higher_items_count = len([
                other
                for other in sorted_items
                if other.get("value", 0) > value
            ])

            place_index = same_or_higher_items_count

            if place_index > 2:
                continue

            bar = PodiumBar(
                name,
                value,
                colors_by_place[place_index],
                heights_by_place[place_index]
            )
            self.highest_rated_games_card.podium_layout.addWidget(bar)
