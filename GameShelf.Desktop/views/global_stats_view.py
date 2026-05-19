from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget
)

from services.statistics_service import get_global_statistics


class GlobalStatsView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.title_label = QLabel("Globalne statystyki")
        self.layout.addWidget(self.title_label)

        self.total_users_label = QLabel()
        self.total_games_label = QLabel()
        self.total_user_games_label = QLabel()

        self.layout.addWidget(self.total_users_label)
        self.layout.addWidget(self.total_games_label)
        self.layout.addWidget(self.total_user_games_label)

        self.popular_games_list = QListWidget()
        self.popular_platforms_list = QListWidget()
        self.popular_genres_list = QListWidget()
        self.highest_rated_games_list = QListWidget()

        self.layout.addWidget(QLabel("Najpopularniejsze gry"))
        self.layout.addWidget(self.popular_games_list)

        self.layout.addWidget(QLabel("Najpopularniejsze platformy"))
        self.layout.addWidget(self.popular_platforms_list)

        self.layout.addWidget(QLabel("Najpopularniejsze gatunki"))
        self.layout.addWidget(self.popular_genres_list)

        self.layout.addWidget(QLabel("Najwyżej oceniane gry"))
        self.layout.addWidget(self.highest_rated_games_list)

        self.load_statistics()

    def load_statistics(self):
        stats = get_global_statistics()

        if not stats:
            self.total_users_label.setText("Nie udało się pobrać statystyk.")
            return

        self.total_users_label.setText(
            f"Liczba użytkowników: {stats.get('totalUsers', 0)}"
        )
        self.total_games_label.setText(
            f"Liczba gier w bibliotece globalnej: {stats.get('totalGamesInLibrary', 0)}"
        )
        self.total_user_games_label.setText(
            f"Liczba gier w kolekcjach użytkowników: {stats.get('totalUserGames', 0)}"
        )

        self.fill_list(self.popular_games_list, stats.get("mostPopularGames", []))
        self.fill_list(self.popular_platforms_list, stats.get("popularPlatforms", []))
        self.fill_list(self.popular_genres_list, stats.get("popularGenres", []))
        self.fill_list(self.highest_rated_games_list, stats.get("highestRatedGames", []))

    def fill_list(self, list_widget, items):
        list_widget.clear()

        if not items:
            list_widget.addItem("Brak danych")
            return

        for item in items:
            label = item.get("label", "Brak")
            value = item.get("value", 0)
            list_widget.addItem(f"{label}: {value}")