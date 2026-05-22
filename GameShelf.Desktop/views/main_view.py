from pathlib import Path

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
    QApplication,
    QFrame
)
from PySide6.QtCore import Qt, QSize, QPoint, QTimer
from PySide6.QtGui import QFontDatabase, QIcon

from utils.window_corners import disable_windows_11_rounded_corners


from services.collections_service import (
    get_my_collection,
    get_sorted_collections,
    get_collections_lookup,
    get_current_collection as find_current_collection,
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
from views.styled_dialog import ask_confirmation, show_info, show_warning
from views.chat_view import ChatView
from components.main_filter_combo_box import MainFilterComboBox
from components.sidebar_widget import SidebarWidget
from components.game_card import AddGameCard, GameCard
from constants.collection_tabs import ALL_COLLECTION_ID, MAIN_COLLECTION_NAME, PROTECTED_COLLECTION_NAMES
from constants.view_indices import (
    CHAT_VIEW_INDEX,
    FRIENDS_VIEW_INDEX,
    GLOBAL_STATS_VIEW_INDEX,
    HOME_VIEW_INDEX,
    NOTIFICATIONS_VIEW_INDEX,
    PROFILE_VIEW_INDEX,
    SETTINGS_VIEW_INDEX,
    STATS_VIEW_INDEX,
)
from services.cover_image_service import CoverImageService
from utils.game_filters import filter_games, get_unique_genres, get_unique_platforms, sort_games

class MainView(QWidget):
    PROFILE_VIEW_INDEX = PROFILE_VIEW_INDEX
    HOME_VIEW_INDEX = HOME_VIEW_INDEX
    FRIENDS_VIEW_INDEX = FRIENDS_VIEW_INDEX
    CHAT_VIEW_INDEX = CHAT_VIEW_INDEX
    NOTIFICATIONS_VIEW_INDEX = NOTIFICATIONS_VIEW_INDEX
    STATS_VIEW_INDEX = STATS_VIEW_INDEX
    GLOBAL_STATS_VIEW_INDEX = GLOBAL_STATS_VIEW_INDEX
    SETTINGS_VIEW_INDEX = SETTINGS_VIEW_INDEX

    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.current_filter = ALL_COLLECTION_ID
        self.collection_buttons = []
        self.all_games = []
        self.base_dir = Path(__file__).resolve().parents[1]
        self.assets_dir = self.base_dir / "assets"
        self.cover_image_service = CoverImageService()

        self.drag_position = QPoint()
        self.is_dragging = False

        self.load_fonts()
        self.setWindowTitle("GameShelf")
        self.setObjectName("mainPage")
        self.setMinimumSize(1180, 720)
        self.resize(1280, 760)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setup_ui()
        self.connect_signals()
        self.load_collection_tabs()
        self.load_games()
        self.switch_view(self.HOME_VIEW_INDEX)
        self.set_active_button(self.home_button)

    def showEvent(self, event):
        super().showEvent(event)
        disable_windows_11_rounded_corners(self)

    def load_fonts(self):
        font_dir = self.base_dir / "assets"

        for font_path in font_dir.glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(font_path))

        for font_path in font_dir.glob("*.otf"):
            QFontDatabase.addApplicationFont(str(font_path))

    def setup_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.main_frame = QFrame()
        self.main_frame.setObjectName("mainFrame")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(28, 24, 28, 28)
        main_layout.setSpacing(18)

        main_layout.addLayout(self.create_window_controls_bar())

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(28)

        sidebar = self.create_sidebar()

        self.stacked_layout = QStackedLayout()
        self.home_widget = self.create_home_widget()

        self.friends_view = FriendsView()
        self.chat_view = ChatView()
        self.stats_view = StatsView()
        self.settings_view = SettingsView()
        self.global_stats_view = GlobalStatsView()
        self.notifications_view = NotificationsView()
        self.profile_view = ProfileView(self.logout_view)

        self.setup_notifications_counter()

        self.stacked_layout.addWidget(self.profile_view)
        self.stacked_layout.addWidget(self.home_widget)
        self.stacked_layout.addWidget(self.friends_view)
        self.stacked_layout.addWidget(self.chat_view)
        self.stacked_layout.addWidget(self.notifications_view)
        self.stacked_layout.addWidget(self.stats_view)
        self.stacked_layout.addWidget(self.global_stats_view)
        self.stacked_layout.addWidget(self.settings_view)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addLayout(self.stacked_layout)

        body_layout.addWidget(sidebar)
        body_layout.addLayout(content_layout, 1)

        main_layout.addLayout(body_layout)
        self.main_frame.setLayout(main_layout)

        outer_layout.addWidget(self.main_frame)
        self.setLayout(outer_layout)


    def setup_notifications_counter(self):
        self.notifications_badge = QLabel(self.notifications_button)
        self.notifications_badge.setObjectName("notificationsBadge")
        self.notifications_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notifications_badge.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.notifications_badge.setFixedSize(19, 19)
        self.notifications_badge.move(33, 1)
        self.notifications_badge.hide()

        self.notifications_view.unread_count_changed.connect(self.update_notifications_badge)
        self.update_notifications_badge(self.notifications_view.get_unread_count())

        self.notifications_timer = QTimer(self)
        self.notifications_timer.setInterval(15000)
        self.notifications_timer.timeout.connect(self.notifications_view.refresh_notifications)
        self.notifications_timer.start()

    def update_notifications_badge(self, count):
        if count <= 0:
            self.notifications_badge.hide()
            return

        if count <= 9:
            self.notifications_badge.setText(str(count))
            self.notifications_badge.setFixedSize(19, 19)
            self.notifications_badge.move(33, 1)
        else:
            self.notifications_badge.setText("9+")
            self.notifications_badge.setFixedSize(22, 19)
            self.notifications_badge.move(30, 1)

        self.notifications_badge.show()
        self.notifications_badge.raise_()

    def create_window_controls_bar(self):
        controls_bar = QHBoxLayout()
        controls_bar.setContentsMargins(0, 0, 6, 0)
        controls_bar.setSpacing(10)

        self.minimize_button = QPushButton("—")
        self.maximize_button = QPushButton("□")
        self.close_button = QPushButton("×")

        self.minimize_button.setObjectName("windowControlButton")
        self.maximize_button.setObjectName("windowControlButton")
        self.close_button.setObjectName("windowCloseButton")

        for button in [self.minimize_button, self.maximize_button, self.close_button]:
            button.setFixedSize(34, 34)

        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.close_button.clicked.connect(self.close)

        controls_bar.addStretch()
        controls_bar.addWidget(self.minimize_button)
        controls_bar.addWidget(self.maximize_button)
        controls_bar.addWidget(self.close_button)

        return controls_bar

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() <= 90:
            self.is_dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() == Qt.LeftButton and not self.isMaximized():
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        event.accept()

    def create_sidebar(self):
        self.sidebar_widget = SidebarWidget(self.assets_dir)
        self.logo_label = self.sidebar_widget.logo_label
        self.profile_button = self.sidebar_widget.profile_button
        self.home_button = self.sidebar_widget.home_button
        self.stats_button = self.sidebar_widget.stats_button
        self.friends_button = self.sidebar_widget.friends_button
        self.chat_button = self.sidebar_widget.chat_button
        self.global_stats_button = self.sidebar_widget.global_stats_button
        self.notifications_button = self.sidebar_widget.notifications_button
        self.settings_button = self.sidebar_widget.settings_button
        self.logout_button = self.sidebar_widget.logout_button
        return self.sidebar_widget

    def create_collection_icon_button(self, icon_name, object_name):
        button = QPushButton()
        button.setObjectName(object_name)
        button.setIcon(QIcon(str(self.base_dir / "assets" / icon_name)))
        button.setIconSize(QSize(22, 22))

        return button

    def create_home_widget(self):
        widget = QWidget()
        widget.setObjectName("homeWidget")

        layout = QVBoxLayout()
        layout.setContentsMargins(34, 22, 34, 22)
        layout.setSpacing(22)

        self.page_title = QLabel("Twoje kolekcje")
        self.page_title.setObjectName("mainPageTitle")
        self.page_title.setAlignment(Qt.AlignCenter)

        self.collection_panel = QFrame()
        self.collection_panel.setObjectName("collectionPanel")

        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(56, 32, 42, 26)
        panel_layout.setSpacing(20)

        tabs_row_layout = QHBoxLayout()
        tabs_row_layout.setContentsMargins(0, 0, 0, 0)
        tabs_row_layout.setSpacing(12)

        self.tabs_scroll_container = QWidget()
        self.tabs_scroll_container.setObjectName("tabsScrollContainer")
        tabs_scroll_container_layout = QHBoxLayout()
        tabs_scroll_container_layout.setContentsMargins(0, 0, 0, 0)
        tabs_scroll_container_layout.setSpacing(0)

        self.tabs_scroll_area = QScrollArea()
        self.tabs_scroll_area.setObjectName("tabsScrollArea")
        self.tabs_scroll_area.setFixedHeight(40)
        self.tabs_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabs_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabs_scroll_area.setWidgetResizable(True)

        self.tabs_scroll_widget = QWidget()
        self.tabs_scroll_widget.setObjectName("tabsScrollWidget")

        self.tabs_layout = QHBoxLayout()
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(26)

        self.tabs_scroll_widget.setLayout(self.tabs_layout)
        self.tabs_scroll_area.setWidget(self.tabs_scroll_widget)

        self.tabs_fade_label = QLabel()
        self.tabs_fade_label.setObjectName("tabsFadeOverlay")
        self.tabs_fade_label.setFixedWidth(48)
        self.tabs_fade_label.setFixedHeight(40)

        tabs_scroll_container_layout.addWidget(self.tabs_scroll_area, 1)
        tabs_scroll_container_layout.addWidget(self.tabs_fade_label)
        self.tabs_scroll_container.setLayout(tabs_scroll_container_layout)

        def tabs_wheel_event(event):
            scroll_bar = self.tabs_scroll_area.horizontalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - event.angleDelta().y())
            self._update_tabs_fade()
        self.tabs_scroll_area.wheelEvent = tabs_wheel_event
        self.tabs_scroll_area.horizontalScrollBar().valueChanged.connect(
            lambda: self._update_tabs_fade()
        )

        self.tab_all = QPushButton(MAIN_COLLECTION_NAME)
        self.tab_all.setObjectName("collectionTab")
        self.add_collection_button = self.create_collection_icon_button("AddGameIcon.svg", "addCollectionIconButton")
        self.edit_collection_button = self.create_collection_icon_button("EditCollectionIcon.svg", "smallIconButton")
        self.delete_collection_button = self.create_collection_icon_button("DeleteCollectionIcon.svg", "smallIconButton")
        self.share_collection_button = self.create_collection_icon_button("CollectionShareCodeIcon.svg", "wideIconButton")

        self.add_collection_button.setFixedSize(24, 24)
        self.edit_collection_button.setFixedSize(36, 36)
        self.delete_collection_button.setFixedSize(36, 36)
        self.share_collection_button.setFixedSize(48, 36)

        tabs_row_layout.addWidget(self.tabs_scroll_container, 1)
        tabs_row_layout.addWidget(self.add_collection_button, 0, Qt.AlignVCenter)

        self.filters_layout = QHBoxLayout()
        self.filters_layout.setContentsMargins(0, 0, 0, 0)
        self.filters_layout.setSpacing(14)

        self.genre_filter = MainFilterComboBox(self.assets_dir)
        self.platform_filter = MainFilterComboBox(self.assets_dir)
        self.sort_filter = MainFilterComboBox(self.assets_dir)

        for combo in [self.genre_filter, self.platform_filter, self.sort_filter]:
            combo.setFixedHeight(36)

        self.genre_filter.setFixedWidth(196)
        self.platform_filter.setFixedWidth(196)
        self.sort_filter.setFixedWidth(226)

        self.genre_filter.addItem("Wszystkie gatunki", ALL_COLLECTION_ID)
        self.platform_filter.addItem("Wszystkie platformy", ALL_COLLECTION_ID)

        self.sort_filter.addItem("Sortuj: tytuł A-Z", "title_asc")
        self.sort_filter.addItem("Sortuj: tytuł Z-A", "title_desc")
        self.sort_filter.addItem("Sortuj: gatunek A-Z", "genre_asc")
        self.sort_filter.addItem("Sortuj: platforma A-Z", "platform_asc")

        self.filters_layout.addWidget(self.genre_filter)
        self.filters_layout.addWidget(self.platform_filter)
        self.filters_layout.addWidget(self.sort_filter)
        self.filters_layout.addStretch()
        self.filters_layout.addWidget(self.edit_collection_button)
        self.filters_layout.addWidget(self.delete_collection_button)
        self.filters_layout.addWidget(self.share_collection_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("gamesScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("gamesScrollWidget")

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 14, 0, 0)
        self.grid_layout.setHorizontalSpacing(22)
        self.grid_layout.setVerticalSpacing(28)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        panel_layout.addLayout(tabs_row_layout)
        panel_layout.addLayout(self.filters_layout)
        panel_layout.addWidget(self.scroll_area)

        self.collection_panel.setLayout(panel_layout)

        layout.addWidget(self.page_title)
        layout.addWidget(self.collection_panel, 1)

        widget.setLayout(layout)

        return widget

    def connect_signals(self):
        self.profile_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.PROFILE_VIEW_INDEX, self.profile_button)
        )
        self.home_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.HOME_VIEW_INDEX, self.home_button)
        )
        self.stats_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.STATS_VIEW_INDEX, self.stats_button)
        )
        self.friends_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.FRIENDS_VIEW_INDEX, self.friends_button)
        )
        self.chat_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.CHAT_VIEW_INDEX, self.chat_button)
        )
        self.global_stats_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.GLOBAL_STATS_VIEW_INDEX, self.global_stats_button)
        )
        self.notifications_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.NOTIFICATIONS_VIEW_INDEX, self.notifications_button)
        )
        self.settings_button.clicked.connect(
            lambda: self.switch_view_with_highlight(self.SETTINGS_VIEW_INDEX, self.settings_button)
        )

        self.logout_button.clicked.connect(self.logout_view)
        self.tab_all.clicked.connect(lambda: self.change_tab(ALL_COLLECTION_ID))
        self.add_collection_button.clicked.connect(self.handle_add_collection)
        self.edit_collection_button.clicked.connect(self.handle_edit_collection)
        self.delete_collection_button.clicked.connect(self.handle_delete_collection)
        self.share_collection_button.clicked.connect(self.handle_share_collection)

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
        self.refresh_active_collection_tab()

    def load_games(self):
        self.all_games = get_my_collection()
        self.refresh_filter_options()
        self.apply_filters()

    def refresh_filter_options(self):
        current_genre = self.genre_filter.currentData()
        current_platform = self.platform_filter.currentData()

        self.genre_filter.blockSignals(True)
        self.platform_filter.blockSignals(True)

        self.genre_filter.clear()
        self.platform_filter.clear()

        self.genre_filter.addItem("Wszystkie gatunki", ALL_COLLECTION_ID)
        self.platform_filter.addItem("Wszystkie platformy", ALL_COLLECTION_ID)

        for genre in get_unique_genres(self.all_games):
            self.genre_filter.addItem(genre, genre)

        for platform in get_unique_platforms(self.all_games):
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
        return filter_games(
            self.all_games,
            self.current_filter,
            self.genre_filter.currentData(),
            self.platform_filter.currentData()
        )


    def get_sorted_games(self, games):
        return sort_games(games, self.sort_filter.currentData())


    def render_games(self, games):
        self.clear_games_grid()

        row = 0
        col = 0

        if self.current_filter != ALL_COLLECTION_ID:
            add_card = self.create_add_game_card()
            self.grid_layout.addWidget(add_card, 0, 0)
            col = 1

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

    def create_add_game_card(self):
        return AddGameCard(self.assets_dir, self.handle_add_game)


    def create_game_card(self, game):
        return GameCard(
            game,
            self.assets_dir,
            self.cover_image_service,
            self.handle_rate_game,
            self.handle_move_game,
            self.handle_remove_game
        )






    def set_active_button(self, active_button):
        buttons = [
            self.profile_button,
            self.home_button,
            self.stats_button,
            self.friends_button,
            self.chat_button,
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

    def refresh_active_collection_tab(self):
        tabs = [self.tab_all] + self.collection_buttons

        for button in tabs:
            button.setProperty("active", False)
            button.style().unpolish(button)
            button.style().polish(button)

        if self.current_filter == ALL_COLLECTION_ID:
            self.tab_all.setProperty("active", True)
            self.tab_all.style().unpolish(self.tab_all)
            self.tab_all.style().polish(self.tab_all)
            return

        for button in self.collection_buttons:
            if button.property("collectionId") == self.current_filter:
                button.setProperty("active", True)
                button.style().unpolish(button)
                button.style().polish(button)
                return

    def _update_tabs_fade(self):
        bar = self.tabs_scroll_area.horizontalScrollBar()
        at_end = bar.value() >= bar.maximum() - 2
        content_overflows = self.tabs_scroll_widget.sizeHint().width() > self.tabs_scroll_area.width()
        self.tabs_fade_label.setVisible(content_overflows and not at_end)

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

        collections = get_sorted_collections()

        for collection in collections:
            collection_id = collection.get("id")
            collection_name = collection.get("name", "Bez nazwy")

            button = QPushButton(collection_name)
            button.setObjectName("collectionTab")
            button.setProperty("collectionId", collection_id)
            button.clicked.connect(
                lambda checked=False, selected_id=collection_id: self.change_tab(selected_id)
            )

            self.collection_buttons.append(button)
            self.tabs_layout.addWidget(button)

        self.tabs_layout.addStretch()
        self.refresh_active_collection_tab()
        QTimer.singleShot(50, self._update_tabs_fade)

    def clear_collection_tabs(self):
        widgets = [
            self.tab_all,
        ]

        for widget in widgets:
            self.tabs_layout.removeWidget(widget)

        for button in self.collection_buttons:
            self.tabs_layout.removeWidget(button)
            button.deleteLater()

        self.collection_buttons.clear()

    def handle_add_game(self):
        if self.current_filter == ALL_COLLECTION_ID:
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
        if not ask_confirmation(self, "Czy na pewno chcesz usunąć tę grę z kolekcji?", "Usuń grę"):
            return

        success = remove_game_from_collection(game_id)

        if not success:
            self.show_warning("Nie udało się usunąć gry z kolekcji.")
            return

        self.load_games()

    def handle_edit_collection(self):
        if self.current_filter == ALL_COLLECTION_ID:
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
        if self.current_filter == ALL_COLLECTION_ID:
            self.show_warning("Nie można usunąć głównej biblioteki.")
            return

        selected_collection = self.get_current_collection()

        if not selected_collection:
            self.show_warning("Nie znaleziono wybranej kolekcji.")
            return

        if self.is_protected_collection(selected_collection.get("name")):
            self.show_warning("Nie można usunąć domyślnej kolekcji.")
            return

        if not ask_confirmation(
            self,
            f"Czy na pewno chcesz usunąć kolekcję „{selected_collection.get('name')}”?",
            "Usuń kolekcję"
        ):
            return

        success = delete_collection(self.current_filter)

        if not success:
            self.show_warning("Nie udało się usunąć kolekcji.")
            return

        self.current_filter = ALL_COLLECTION_ID
        self.load_collection_tabs()
        self.load_games()

    def get_current_collection(self):
        return find_current_collection(self.current_filter)


    def is_protected_collection(self, collection_name):
        return collection_name in PROTECTED_COLLECTION_NAMES


    def show_warning(self, message):
        show_warning(self, message)

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

        show_info(self, "Ocena została zapisana.")

    def handle_share_collection(self):
        if self.current_filter == ALL_COLLECTION_ID:
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

        QApplication.clipboard().setText(share_code)

        show_info(self, f"Kod udostępniania kolekcji został skopiowany do schowka:\n\n{share_code}")
