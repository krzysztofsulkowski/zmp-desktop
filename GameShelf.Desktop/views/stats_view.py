from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget
)

from services.statistics_service import get_my_library_statistics


class StatsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("statsView")

        self.layout = QVBoxLayout(self)

        self.title_label = QLabel("Twoje statystyki")
        self.title_label.setObjectName("pageTitle")
        self.layout.addWidget(self.title_label)

        self.total_games_label = QLabel()
        self.layout.addWidget(self.total_games_label)

        self.added_recently_label = QLabel()
        self.layout.addWidget(self.added_recently_label)

        self.genres_list = QListWidget()
        self.layout.addWidget(self.genres_list)

        self.platforms_list = QListWidget()
        self.layout.addWidget(self.platforms_list)

        self.collections_list = QListWidget()
        self.layout.addWidget(self.collections_list)

        self.load_statistics()

    def load_statistics(self):
        stats = get_my_library_statistics()

        if not stats:
            self.total_games_label.setText("Nie udało się pobrać statystyk.")
            return

        total_games = stats.get("totalGames", 0)
        added_recently = stats.get("addedRecentlyCount", 0)

        self.total_games_label.setText(
            f"Liczba gier: {total_games}"
        )

        self.added_recently_label.setText(
            f"Ostatnio dodane: {added_recently}"
        )

        genres = stats.get("gamesByGenre", [])

        for genre in genres:
            label = genre.get("label", "Brak")
            value = genre.get("value", 0)

            self.genres_list.addItem(
                f"{label}: {value}"
            )

        platforms = stats.get("gamesByPlatform", [])

        for platform in platforms:
            label = platform.get("label", "Brak")
            value = platform.get("value", 0)

            self.platforms_list.addItem(
                f"{label}: {value}"
            )

        collections = stats.get("gamesByCollection", [])

        for collection in collections:
            label = collection.get("label", "Brak")
            value = collection.get("value", 0)

            self.collections_list.addItem(
                f"{label}: {value}"
            )