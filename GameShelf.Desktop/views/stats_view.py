from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea

from components.stats_widgets import DonutChartWidget, StatsCard
from services.statistics_service import get_my_library_statistics


class StatsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("statsView")
        self.cards = []
        self.current_columns = 0

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(36, 28, 36, 28)
        self.main_layout.setSpacing(26)

        self.title_label = QLabel("Twoje statystyki")
        self.title_label.setObjectName("statsPageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("statsScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("statsScrollWidget")
        self.grid = QGridLayout(self.scroll_widget)
        self.grid.setContentsMargins(0, 0, 0, 24)
        self.grid.setHorizontalSpacing(14)
        self.grid.setVerticalSpacing(26)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.total_card, self.total_value_label = self.create_number_card(
            "posiadasz następującą liczbę gier w swojej bibliotece:"
        )
        self.recent_card, self.recent_value_label = self.create_number_card(
            "liczba ostatnio dodanych gier w Twojej bibliotece:"
        )
        self.genre_card, self.genre_chart = self.create_chart_card(
            "liczba gier z podziałem na kategorie:"
        )
        self.platform_card, self.platform_chart = self.create_chart_card(
            "liczba gier z podziałem na platformy:"
        )
        self.collection_card, self.collection_chart = self.create_chart_card(
            "liczba gier z podziałem na kolekcje:"
        )

        self.cards = [
            self.total_card,
            self.recent_card,
            self.genre_card,
            self.platform_card,
            self.collection_card,
        ]

        self.rebuild_grid(3)
        self.load_statistics()

    def create_number_card(self, title):
        card = StatsCard(title)

        value_label = QLabel("0")
        value_label.setObjectName("statsNumber")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card.layout.addStretch(1)
        card.layout.addWidget(value_label)
        card.layout.addStretch(2)

        return card, value_label

    def create_chart_card(self, title):
        card = StatsCard(title)

        chart = DonutChartWidget()
        card.layout.addWidget(chart, 1)

        return card, chart

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grid_columns()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_grid_columns()
        self.load_statistics()

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

    def rebuild_grid(self, columns):
        if self.current_columns == columns:
            return

        self.current_columns = columns

        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for index, card in enumerate(self.cards):
            row = index // columns
            column = index % columns
            self.grid.addWidget(card, row, column, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def load_statistics(self):
        stats = get_my_library_statistics()

        if not stats:
            self.total_value_label.setText("-")
            self.recent_value_label.setText("-")
            return

        self.total_value_label.setText(str(stats.get("totalGames", 0)))
        self.recent_value_label.setText(str(stats.get("addedRecentlyCount", 0)))

        self.genre_chart.set_data(stats.get("gamesByGenre", []))
        self.platform_chart.set_data(stats.get("gamesByPlatform", []))
        self.collection_chart.set_data(stats.get("gamesByCollection", []))
