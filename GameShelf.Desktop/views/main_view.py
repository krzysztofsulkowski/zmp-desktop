from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QGridLayout,
    QStackedLayout,
    QDialog,
    QMessageBox,
    QComboBox,
    QApplication
)

from config import API_URL

from services.collection_service import (
    get_my_collection,
    get_collections_lookup,
    create_collection,
    update_collection,
    delete_collection
)
from services.session import clear_token
from services.auth_service import logout
from services.game_service import (
    get_available_games,
    add_game_to_collection,
    remove_game_from_collection,
    move_game,
    rate_game
)
from services.share_code_store import get_share_code

from views.profile_view import ProfileView
from views.friends_view import FriendsView
from views.stats_view import StatsView
from views.settings_view import SettingsView
from views.global_stats_view import GlobalStatsView
from views.notifications_view import NotificationsView
from views.logout_dialog import LogoutDialog
from views.create_collection_dialog import CreateCollectionDialog
from views.add_game_dialog import AddGameDialog
from views.edit_collection_dialog import EditCollectionDialog
from views.move_game_dialog import MoveGameDialog
from views.rate_game_dialog import RateGameDialog


class MainView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.current_filter = "all"
        self.collection_buttons = []
        self.all_games = []

        self.setWindowTitle("GameShelf")

        self.setup_ui()
        self.connect_signals()
        self.load_collection_tabs()
        self.load_games()
        self.set_active_button(self.home_button)

    def setup_ui(self):
        main_layout = QHBoxLayout()
        sidebar = self.create_sidebar()

        self.stacked_layout = QStackedLayout()
        self.home_widget = self.create_home_widget()

        self.friends_view = FriendsView()
        self.stats_view = StatsView()
        self.settings_view = SettingsView()
        self.global_stats_view = GlobalStatsView()
        self.notifications_view = NotificationsView()
        self.profile_view = ProfileView(self.logout_view)

        self.stacked_layout.addWidget(self.home_widget)
        self.stacked_layout.addWidget(self.friends_view)
        self.stacked_layout.addWidget(self.stats_view)
        self.stacked_layout.addWidget(self.settings_view)
        self.stacked_layout.addWidget(self.global_stats_view)
        self.stacked_layout.addWidget(self.notifications_view)
        self.stacked_layout.addWidget(self.profile_view)

        content_layout = QVBoxLayout()
        content_layout.addLayout(self.stacked_layout)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(content_layout, 4)

        self.setLayout(main_layout)

    def create_sidebar(self):
        sidebar = QVBoxLayout()

        self.profile_button = QPushButton("Profil")
        self.home_button = QPushButton("Biblioteka")
        self.stats_button = QPushButton("Statystyki")
        self.friends_button = QPushButton("Znajomi")
        self.global_stats_button = QPushButton("Statystyki globalne")
        self.notifications_button = QPushButton("Powiadomienia")
        self.settings_button = QPushButton("Ustawienia")
        self.logout_button = QPushButton("Wyloguj")

        sidebar.addWidget(self.profile_button)
        sidebar.addWidget(self.home_button)
        sidebar.addWidget(self.stats_button)
        sidebar.addWidget(self.friends_button)
        sidebar.addWidget(self.global_stats_button)
        sidebar.addWidget(self.notifications_button)
        sidebar.addWidget(self.settings_button)
        sidebar.addStretch()
        sidebar.addWidget(self.logout_button)

        return sidebar

    def create_home_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.tabs_layout = QHBoxLayout()

        self.tab_all = QPushButton("Biblioteka")
        self.add_collection_button = QPushButton("+")
        self.edit_collection_button = QPushButton("Edytuj")
        self.delete_collection_button = QPushButton("Usuń")
        self.share_collection_button = QPushButton("Udostępnij")

        self.add_collection_button.setFixedSize(32, 32)
        self.edit_collection_button.setFixedSize(70, 32)
        self.delete_collection_button.setFixedSize(70, 32)
        self.share_collection_button.setFixedSize(100, 32)

        self.filters_layout = QHBoxLayout()

        self.genre_filter = QComboBox()
        self.platform_filter = QComboBox()
        self.sort_filter = QComboBox()

        self.genre_filter.addItem("Wszystkie gatunki", "all")
        self.platform_filter.addItem("Wszystkie platformy", "all")

        self.sort_filter.addItem("Sortuj: tytuł A-Z", "title_asc")
        self.sort_filter.addItem("Sortuj: tytuł Z-A", "title_desc")
        self.sort_filter.addItem("Sortuj: gatunek A-Z", "genre_asc")
        self.sort_filter.addItem("Sortuj: platforma A-Z", "platform_asc")

        self.filters_layout.addWidget(self.genre_filter)
        self.filters_layout.addWidget(self.platform_filter)
        self.filters_layout.addWidget(self.sort_filter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout()

        self.scroll_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.add_game_button = QPushButton("Dodaj grę")

        layout.addLayout(self.tabs_layout)
        layout.addLayout(self.filters_layout)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.add_game_button)

        widget.setLayout(layout)

        return widget

    def connect_signals(self):
        self.profile_button.clicked.connect(
            lambda: self.switch_view_with_highlight(6, self.profile_button)
        )
        self.home_button.clicked.connect(
            lambda: self.switch_view_with_highlight(0, self.home_button)
        )
        self.friends_button.clicked.connect(
            lambda: self.switch_view_with_highlight(1, self.friends_button)
        )
        self.stats_button.clicked.connect(
            lambda: self.switch_view_with_highlight(2, self.stats_button)
        )
        self.settings_button.clicked.connect(
            lambda: self.switch_view_with_highlight(3, self.settings_button)
        )
        self.global_stats_button.clicked.connect(
            lambda: self.switch_view_with_highlight(4, self.global_stats_button)
        )
        self.notifications_button.clicked.connect(
            lambda: self.switch_view_with_highlight(5, self.notifications_button)
        )

        self.logout_button.clicked.connect(self.logout_view)
        self.tab_all.clicked.connect(lambda: self.change_tab("all"))
        self.add_collection_button.clicked.connect(self.handle_add_collection)
        self.edit_collection_button.clicked.connect(self.handle_edit_collection)
        self.delete_collection_button.clicked.connect(self.handle_delete_collection)
        self.share_collection_button.clicked.connect(self.handle_share_collection)
        self.add_game_button.clicked.connect(self.handle_add_game)

        self.genre_filter.currentIndexChanged.connect(self.apply_filters)
        self.platform_filter.currentIndexChanged.connect(self.apply_filters)
        self.sort_filter.currentIndexChanged.connect(self.apply_filters)

    def switch_view(self, index):
        self.stacked_layout.setCurrentIndex(index)

    def switch_view_with_highlight(self, index, button):
        self.switch_view(index)
        self.set_active_button(button)

    def logout_view(self):
        dialog = LogoutDialog()
        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        logout()
        clear_token()
        self.controller.show_login()

    def change_tab(self, tab):
        self.current_filter = tab
        self.apply_filters()

    def load_games(self):
        self.all_games = get_my_collection()
        self.refresh_filter_options()
        self.apply_filters()

    def refresh_filter_options(self):
        current_genre = self.genre_filter.currentData()
        current_platform = self.platform_filter.currentData()

        genres = sorted({
            game.genre
            for game in self.all_games
            if game.genre
        })

        platforms = sorted({
            game.platform
            for game in self.all_games
            if game.platform
        })

        self.genre_filter.blockSignals(True)
        self.platform_filter.blockSignals(True)

        self.genre_filter.clear()
        self.platform_filter.clear()

        self.genre_filter.addItem("Wszystkie gatunki", "all")
        self.platform_filter.addItem("Wszystkie platformy", "all")

        for genre in genres:
            self.genre_filter.addItem(genre, genre)

        for platform in platforms:
            self.platform_filter.addItem(platform, platform)

        self.restore_combo_value(self.genre_filter, current_genre)
        self.restore_combo_value(self.platform_filter, current_platform)

        self.genre_filter.blockSignals(False)
        self.platform_filter.blockSignals(False)

    def restore_combo_value(self, combo_box, value):
        index = combo_box.findData(value)

        if index >= 0:
            combo_box.setCurrentIndex(index)

    def apply_filters(self):
        games = self.get_filtered_games()
        games = self.get_sorted_games(games)

        self.render_games(games)

    def get_filtered_games(self):
        selected_genre = self.genre_filter.currentData()
        selected_platform = self.platform_filter.currentData()

        games = []

        for game in self.all_games:
            if self.current_filter != "all" and game.collection_id != self.current_filter:
                continue

            if selected_genre != "all" and game.genre != selected_genre:
                continue

            if selected_platform != "all" and game.platform != selected_platform:
                continue

            games.append(game)

        return games

    def get_sorted_games(self, games):
        sort_value = self.sort_filter.currentData()

        if sort_value == "title_desc":
            return sorted(games, key=lambda game: game.title.lower(), reverse=True)

        if sort_value == "genre_asc":
            return sorted(games, key=lambda game: (game.genre or "").lower())

        if sort_value == "platform_asc":
            return sorted(games, key=lambda game: (game.platform or "").lower())

        return sorted(games, key=lambda game: game.title.lower())

    def render_games(self, games):
        self.clear_games_grid()

        if not games:
            empty_label = QLabel("Brak gier do wyświetlenia.")
            empty_label.setObjectName("emptyState")
            self.grid_layout.addWidget(empty_label, 0, 0)
            return

        row = 0
        col = 0

        for game in games:
            card = self.create_game_card(game)
            self.grid_layout.addWidget(card, row, col)

            col += 1

            if col == 3:
                col = 0
                row += 1

    def clear_games_grid(self):
        for index in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(index)
            widget = item.widget()

            if widget:
                widget.setParent(None)

    def create_game_card(self, game):
        card = QWidget()
        layout = QVBoxLayout()

        title = QLabel(game.title)
        genre = QLabel(f"Gatunek: {game.genre or 'brak danych'}")
        platform = QLabel(f"Platforma: {game.platform or 'brak danych'}")

        card.setObjectName("gameCard")
        title.setObjectName("gameTitle")
        genre.setObjectName("gameGenre")
        platform.setObjectName("gamePlatform")

        layout.addWidget(title)
        layout.addWidget(genre)
        layout.addWidget(platform)

        rating_text = game.rating if game.rating else "brak"
        rating_label = QLabel(f"Ocena: {rating_text}")

        rating_label.setObjectName("gameRating")

        layout.addWidget(rating_label)

        if self.current_filter != "all":
            rate_button = QPushButton("Oceń")
            move_button = QPushButton("Przenieś")
            remove_button = QPushButton("Usuń")

            rate_button.clicked.connect(
                lambda checked=False, game_obj=game: self.handle_rate_game(game_obj)
            )

            move_button.clicked.connect(
                lambda checked=False, game_obj=game: self.handle_move_game(game_obj)
            )

            remove_button.clicked.connect(
                lambda checked=False, game_id=game.game_id: self.handle_remove_game(game_id)
            )

            layout.addWidget(rate_button)
            layout.addWidget(move_button)
            layout.addWidget(remove_button)

        card.setLayout(layout)
        card.setFixedSize(220, 260)

        return card

    def set_active_button(self, active_button):
        buttons = [
            self.profile_button,
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

    def handle_add_collection(self):
        dialog = CreateCollectionDialog()
        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        name, is_public = dialog.get_collection_data()

        if not name:
            self.show_warning("Nazwa kolekcji jest wymagana.")
            return

        success = create_collection(name, is_public)

        if not success:
            self.show_warning("Nie udało się utworzyć kolekcji.")
            return

        self.load_collection_tabs()
        self.load_games()

    def load_collection_tabs(self):
        self.clear_collection_tabs()

        self.tabs_layout.addWidget(self.tab_all)

        collections = get_collections_lookup()

        for collection in collections:
            collection_id = collection.get("id")
            collection_name = collection.get("name", "Bez nazwy")

            button = QPushButton(collection_name)
            button.clicked.connect(
                lambda checked=False, selected_id=collection_id: self.change_tab(selected_id)
            )

            self.collection_buttons.append(button)
            self.tabs_layout.addWidget(button)

        self.tabs_layout.addWidget(self.edit_collection_button)
        self.tabs_layout.addWidget(self.delete_collection_button)
        self.tabs_layout.addWidget(self.share_collection_button)
        self.tabs_layout.addWidget(self.add_collection_button)

    def clear_collection_tabs(self):
        widgets = [
            self.tab_all,
            self.edit_collection_button,
            self.delete_collection_button,
            self.share_collection_button,
            self.add_collection_button
        ]

        for widget in widgets:
            self.tabs_layout.removeWidget(widget)

        for button in self.collection_buttons:
            self.tabs_layout.removeWidget(button)
            button.deleteLater()

        self.collection_buttons.clear()

    def handle_add_game(self):
        if self.current_filter == "all":
            self.show_warning("Najpierw wybierz konkretną kolekcję.")
            return

        games = get_available_games()

        if not games:
            self.show_warning("Nie znaleziono dostępnych gier do dodania.")
            return

        dialog = AddGameDialog(games)
        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        selected_game = dialog.get_selected_game()

        if not selected_game:
            return

        game_id = selected_game.get("id")
        success = add_game_to_collection(game_id, self.current_filter)

        if not success:
            self.show_warning("Nie udało się dodać gry do kolekcji.")
            return

        self.load_games()

    def handle_remove_game(self, game_id):
        confirmation = QMessageBox.question(
            self,
            "Usuń grę",
            "Czy na pewno chcesz usunąć tę grę z kolekcji?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        success = remove_game_from_collection(game_id)

        if not success:
            self.show_warning("Nie udało się usunąć gry z kolekcji.")
            return

        self.load_games()

    def handle_edit_collection(self):
        if self.current_filter == "all":
            self.show_warning("Najpierw wybierz kolekcję do edycji.")
            return

        selected_collection = self.get_current_collection()

        if not selected_collection:
            self.show_warning("Nie znaleziono wybranej kolekcji.")
            return

        dialog = EditCollectionDialog(
            selected_collection.get("name", ""),
            selected_collection.get("isPublic", True)
        )

        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        name, is_public = dialog.get_collection_data()

        if not name:
            self.show_warning("Nazwa kolekcji jest wymagana.")
            return

        success = update_collection(self.current_filter, name, is_public)

        if not success:
            self.show_warning("Nie udało się zaktualizować kolekcji.")
            return

        self.load_collection_tabs()
        self.load_games()

    def handle_delete_collection(self):
        if self.current_filter == "all":
            self.show_warning("Nie można usunąć głównej biblioteki.")
            return

        selected_collection = self.get_current_collection()

        if not selected_collection:
            self.show_warning("Nie znaleziono wybranej kolekcji.")
            return

        if self.is_protected_collection(selected_collection.get("name")):
            self.show_warning("Nie można usunąć domyślnej kolekcji.")
            return

        confirmation = QMessageBox.question(
            self,
            "Usuń kolekcję",
            f"Czy na pewno chcesz usunąć kolekcję „{selected_collection.get('name')}”?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        success = delete_collection(self.current_filter)

        if not success:
            self.show_warning("Nie udało się usunąć kolekcji.")
            return

        self.current_filter = "all"
        self.load_collection_tabs()
        self.load_games()

    def get_current_collection(self):
        collections = get_collections_lookup()

        for collection in collections:
            if collection.get("id") == self.current_filter:
                return collection

        return None

    def is_protected_collection(self, collection_name):
        protected_collections = [
            "Ulubione",
            "Planowane",
            "Lista życzeń",
            "W trakcie",
            "Ukończone",
            "Porzucone"
        ]

        return collection_name in protected_collections

    def show_warning(self, message):
        QMessageBox.warning(self, "GameShelf", message)

    def handle_move_game(self, game):
        collections = get_collections_lookup()

        dialog = MoveGameDialog(
            collections,
            self.current_filter
        )

        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        target_collection_id = dialog.get_selected_collection_id()

        if not target_collection_id:
            self.show_warning("Wybierz kolekcję docelową.")
            return

        success = move_game(
            game.game_id,
            self.current_filter,
            target_collection_id
        )

        if not success:
            self.show_warning("Nie udało się przenieść gry.")
            return

        self.load_games()

    def handle_rate_game(self, game):
        dialog = RateGameDialog(game.rating)

        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        rating = dialog.get_rating()

        success, error = rate_game(
            game.game_id,
            rating
        )

        if not success:
            self.show_warning(f"Nie udało się zapisać oceny.\n\n{error}")
            return

        for existing_game in self.all_games:
            if existing_game.game_id == game.game_id:
                existing_game.rating = rating

        self.apply_filters()

        QMessageBox.information(
            self,
            "GameShelf",
            "Ocena została zapisana."
        )

    def handle_share_collection(self):
        if self.current_filter == "all":
            self.show_warning("Najpierw wybierz konkretną kolekcję.")
            return

        selected_collection = self.get_current_collection()

        if not selected_collection:
            self.show_warning("Nie znaleziono wybranej kolekcji.")
            return

        if not selected_collection.get("isPublic", False):
            self.show_warning("Kolekcja musi być publiczna, żeby można było ją udostępnić.")
            return

        share_code = get_share_code(self.current_filter)

        if not share_code:
            self.show_warning(
                "Nie udało się pobrać kodu udostępniania dla tej kolekcji. "
                "API zwraca shareCode tylko przy tworzeniu kolekcji, więc działa to dla kolekcji utworzonych od teraz w desktopie."
            )
            return

        share_link = f"{API_URL}/api/collections/share/{share_code}"

        QApplication.clipboard().setText(share_link)

        QMessageBox.information(
            self,
            "GameShelf",
            f"Link do kolekcji został skopiowany do schowka:\n\n{share_link}"
        )