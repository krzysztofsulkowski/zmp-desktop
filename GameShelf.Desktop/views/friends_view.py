from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
    QApplication,
    QFrame,
    QGridLayout,
    QScrollArea
)

from config import WEB_REGISTER_URL
from services.api_client import get_me
from services.friends_service import (
    get_my_friends,
    search_users,
    add_friend_by_username,
    get_pending_requests,
    accept_friend_request,
    reject_or_remove_friend,
    get_friend_collections_with_games,
    compare_with_friend
)


class FriendsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("friendsView")

        self.search_results = []
        self.pending_requests = []
        self.friends = []

        self.current_user = {}
        self.load_current_user()

        self.setup_ui()
        self.connect_signals()
        self.load_friends()
        self.load_pending_requests()

    def setup_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        main_layout = QVBoxLayout(scroll_content)

        main_layout.setContentsMargins(42, 24, 42, 32)
        main_layout.setSpacing(22)

        self.title_label = QLabel("Znajomi")
        self.title_label.setObjectName("friendsPageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setObjectName("friendsStatusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_card = QFrame()
        search_card.setObjectName("friendsCard")

        search_card_layout = QVBoxLayout(search_card)
        search_card_layout.setContentsMargins(22, 18, 22, 22)
        search_card_layout.setSpacing(14)

        search_title = QLabel("Wyszukaj użytkownika")
        search_title.setObjectName("friendsSectionTitle")

        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("friendsSearchInput")
        self.search_input.setPlaceholderText("Wpisz nazwę użytkownika")

        self.search_button = QPushButton("Szukaj")
        self.search_button.setObjectName("friendsPrimaryButton")

        self.add_button = QPushButton("Dodaj wybranego")
        self.add_button.setObjectName("friendsSecondaryButton")

        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.add_button)

        self.search_results_list = QListWidget()
        self.search_results_list.setObjectName("friendsList")
        self.search_results_list.setMinimumHeight(92)

        search_card_layout.addWidget(search_title)
        search_card_layout.addLayout(search_layout)
        search_card_layout.addWidget(self.search_results_list)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        requests_card = QFrame()
        requests_card.setObjectName("friendsCard")
        requests_layout = QVBoxLayout(requests_card)
        requests_layout.setContentsMargins(22, 18, 22, 22)
        requests_layout.setSpacing(14)

        self.pending_label = QLabel("Zaproszenia oczekujące")
        self.pending_label.setObjectName("friendsSectionTitle")

        self.pending_list = QListWidget()
        self.pending_list.setObjectName("friendsList")
        self.pending_list.setMinimumHeight(130)

        pending_buttons_layout = QHBoxLayout()
        pending_buttons_layout.setSpacing(10)

        self.accept_button = QPushButton("Akceptuj")
        self.accept_button.setObjectName("friendsPrimaryButton")

        self.reject_button = QPushButton("Odrzuć")
        self.reject_button.setObjectName("friendsDangerButton")

        pending_buttons_layout.addWidget(self.accept_button)
        pending_buttons_layout.addWidget(self.reject_button)

        requests_layout.addWidget(self.pending_label)
        requests_layout.addWidget(self.pending_list)
        requests_layout.addLayout(pending_buttons_layout)

        friends_card = QFrame()
        friends_card.setObjectName("friendsCard")
        friends_layout = QVBoxLayout(friends_card)
        friends_layout.setContentsMargins(22, 18, 22, 22)
        friends_layout.setSpacing(14)

        self.friends_label = QLabel("Twoi znajomi")
        self.friends_label.setObjectName("friendsSectionTitle")

        self.friends_list = QListWidget()
        self.friends_list.setObjectName("friendsList")
        self.friends_list.setMinimumHeight(130)

        friend_buttons_layout = QGridLayout()
        friend_buttons_layout.setHorizontalSpacing(10)
        friend_buttons_layout.setVerticalSpacing(10)

        self.view_collections_button = QPushButton("Pokaż kolekcje")
        self.view_collections_button.setObjectName("friendsSecondaryButton")

        self.compare_button = QPushButton("Porównaj biblioteki")
        self.compare_button.setObjectName("friendsPrimaryButton")

        self.remove_friend_button = QPushButton("Usuń znajomego")
        self.remove_friend_button.setObjectName("friendsDangerButton")

        self.invite_link_button = QPushButton("Kopiuj link zaproszenia")
        self.invite_link_button.setObjectName("friendsSecondaryButton")

        friend_buttons_layout.addWidget(self.view_collections_button, 0, 0)
        friend_buttons_layout.addWidget(self.compare_button, 0, 1)
        friend_buttons_layout.addWidget(self.remove_friend_button, 1, 0)
        friend_buttons_layout.addWidget(self.invite_link_button, 1, 1)

        friends_layout.addWidget(self.friends_label)
        friends_layout.addWidget(self.friends_list)
        friends_layout.addLayout(friend_buttons_layout)

        grid.addWidget(requests_card, 0, 0)
        grid.addWidget(friends_card, 0, 1)

        details_grid = QGridLayout()
        details_grid.setContentsMargins(0, 0, 0, 0)
        details_grid.setHorizontalSpacing(18)
        details_grid.setVerticalSpacing(18)

        collections_card = QFrame()
        collections_card.setObjectName("friendsCard")
        collections_layout = QVBoxLayout(collections_card)
        collections_layout.setContentsMargins(22, 18, 22, 22)
        collections_layout.setSpacing(14)

        self.friend_collections_label = QLabel("Kolekcje znajomego")
        self.friend_collections_label.setObjectName("friendsSectionTitle")

        self.friend_collections_list = QListWidget()
        self.friend_collections_list.setObjectName("friendsList")
        self.friend_collections_list.setMinimumHeight(190)

        collections_layout.addWidget(self.friend_collections_label)
        collections_layout.addWidget(self.friend_collections_list)

        compare_card = QFrame()
        compare_card.setObjectName("friendsCard")
        compare_layout = QVBoxLayout(compare_card)
        compare_layout.setContentsMargins(22, 18, 22, 22)
        compare_layout.setSpacing(14)

        self.compare_results_label = QLabel("Porównanie bibliotek")
        self.compare_results_label.setObjectName("friendsSectionTitle")

        compare_hint = QLabel("Wybierz znajomego i kliknij „Porównaj biblioteki”, żeby zobaczyć wspólne gry i kolekcje.")
        compare_hint.setObjectName("friendsHintLabel")
        compare_hint.setWordWrap(True)

        self.compare_results_list = QListWidget()
        self.compare_results_list.setObjectName("friendsCompareList")
        self.compare_results_list.setMinimumHeight(190)

        compare_layout.addWidget(self.compare_results_label)
        compare_layout.addWidget(compare_hint)
        compare_layout.addWidget(self.compare_results_list)

        details_grid.addWidget(collections_card, 0, 0)
        details_grid.addWidget(compare_card, 0, 1)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(search_card)
        main_layout.addLayout(grid)
        main_layout.addLayout(details_grid, 1)
        main_layout.addWidget(self.status_label)

        scroll_area.setWidget(scroll_content)
        root_layout.addWidget(scroll_area)

    def connect_signals(self):
        self.search_button.clicked.connect(self.handle_search)
        self.add_button.clicked.connect(self.handle_add_selected_friend)
        self.accept_button.clicked.connect(self.handle_accept_selected_request)
        self.reject_button.clicked.connect(self.handle_reject_selected_request)
        self.view_collections_button.clicked.connect(self.handle_view_friend_collections)
        self.compare_button.clicked.connect(self.handle_compare_friend)
        self.remove_friend_button.clicked.connect(self.handle_remove_selected_friend)
        self.invite_link_button.clicked.connect(self.handle_copy_invite_link)

    def add_simple_item(self, list_widget, text):
        item = QListWidgetItem(text)
        list_widget.addItem(item)

    def add_compare_item(self, title, genre, owned_by_me, owned_by_friend, my_collection, friend_collection):
        item = QListWidgetItem()
        item.setSizeHint(item.sizeHint())

        widget = QFrame()
        widget.setObjectName("compareResultItem")

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("compareResultTitle")
        title_label.setWordWrap(True)

        meta_label = QLabel(genre or "Brak gatunku")
        meta_label.setObjectName("compareResultMeta")

        chips_layout = QHBoxLayout()
        chips_layout.setContentsMargins(0, 2, 0, 4)
        chips_layout.setSpacing(8)

        if owned_by_me:
            chips_layout.addWidget(self.create_chip(f"U mnie: {my_collection}"))

        if owned_by_friend:
            chips_layout.addWidget(self.create_chip(f"U znajomego: {friend_collection}"))

        chips_layout.addStretch()

        layout.addWidget(title_label)
        layout.addWidget(meta_label)
        layout.addLayout(chips_layout)

        widget.adjustSize()
        item.setSizeHint(QSize(0, max(96, widget.sizeHint().height() + 14)))
        self.compare_results_list.addItem(item)
        self.compare_results_list.setItemWidget(item, widget)

    def create_chip(self, text):
        label = QLabel(text)
        label.setObjectName("compareChip")
        label.setWordWrap(True)
        label.setMinimumHeight(30)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setContentsMargins(0, 0, 0, 0)
        return label

    def load_friends(self):
        self.friends_list.clear()
        self.friend_collections_list.clear()
        self.compare_results_list.clear()

        self.friends = get_my_friends()

        if not self.friends:
            self.add_simple_item(self.friends_list, "Brak znajomych")
            return

        for friend in self.friends:
            username = friend.get("userName", "Nieznany użytkownik")
            self.add_simple_item(self.friends_list, username)

    def load_pending_requests(self):
        self.pending_list.clear()

        self.pending_requests = get_pending_requests()

        if not self.pending_requests:
            self.add_simple_item(self.pending_list, "Brak zaproszeń")
            return

        for request in self.pending_requests:
            username = request.get("userName", "Nieznany użytkownik")
            self.add_simple_item(self.pending_list, username)

    def handle_search(self):
        search_value = self.search_input.text().strip()

        if not search_value:
            self.set_status("Wpisz nazwę użytkownika.")
            return

        self.search_results = search_users(search_value)
        self.search_results_list.clear()

        if not self.search_results:
            self.add_simple_item(self.search_results_list, "Brak wyników")
            self.set_status("Nie znaleziono użytkowników.")
            return

        for user in self.search_results:
            username = user.get("userName", "Nieznany użytkownik")
            email = user.get("email")

            if email:
                self.add_simple_item(self.search_results_list, f"{username} ({email})")
            else:
                self.add_simple_item(self.search_results_list, username)

        self.set_status("Wyniki wyszukiwania zostały pobrane.")

    def handle_add_selected_friend(self):
        selected_user = self.get_selected_search_result()

        if not selected_user:
            return

        username = selected_user.get("userName")

        if not username:
            self.set_status("Nie udało się pobrać nazwy użytkownika.")
            return

        success, message = add_friend_by_username(username)
        self.set_status(message)

        if success:
            self.load_pending_requests()
            self.load_friends()

    def handle_accept_selected_request(self):
        selected_request = self.get_selected_pending_request()

        if not selected_request:
            return

        requester_id = selected_request.get("userId") or selected_request.get("id")

        if not requester_id:
            self.set_status("Nie udało się pobrać ID zapraszającego.")
            return

        success, message = accept_friend_request(requester_id)
        self.set_status(message)

        if success:
            self.load_pending_requests()
            self.load_friends()

    def handle_reject_selected_request(self):
        selected_request = self.get_selected_pending_request()

        if not selected_request:
            return

        requester_id = selected_request.get("userId") or selected_request.get("id")

        if not requester_id:
            self.set_status("Nie udało się pobrać ID zapraszającego.")
            return

        success, message = reject_or_remove_friend(requester_id)
        self.set_status(message)

        if success:
            self.load_pending_requests()
            self.load_friends()

    def handle_remove_selected_friend(self):
        selected_friend = self.get_selected_friend()

        if not selected_friend:
            return

        friend_id = selected_friend.get("userId") or selected_friend.get("id")

        if not friend_id:
            self.set_status("Nie udało się pobrać ID znajomego.")
            return

        success, message = reject_or_remove_friend(friend_id)
        self.set_status(message)

        if success:
            self.load_friends()

    def handle_view_friend_collections(self):
        selected_friend = self.get_selected_friend()

        if not selected_friend:
            return

        friend_id = selected_friend.get("userId") or selected_friend.get("id")

        if not friend_id:
            self.set_status("Nie udało się pobrać ID znajomego.")
            return

        collections = get_friend_collections_with_games(friend_id)

        self.friend_collections_list.clear()

        if not collections:
            self.add_simple_item(self.friend_collections_list, "Brak publicznych kolekcji")
            self.set_status("Znajomy nie ma publicznych kolekcji.")
            return

        for collection in collections:
            collection_name = collection.get("collectionName", "Bez nazwy")
            games = collection.get("games", [])

            self.add_simple_item(
                self.friend_collections_list,
                f"{collection_name} ({len(games)} gier)"
            )

            for game in games:
                title = game.get("title", "Bez tytułu")
                self.add_simple_item(self.friend_collections_list, f"  • {title}")

        self.set_status("Kolekcje znajomego pobrane.")

    def handle_compare_friend(self):
        selected_friend = self.get_selected_friend()

        if not selected_friend:
            return

        friend_id = selected_friend.get("userId") or selected_friend.get("id")

        if not friend_id:
            self.set_status("Nie udało się pobrać ID znajomego.")
            return

        compare_result = compare_with_friend(friend_id)

        self.compare_results_list.clear()

        if not compare_result:
            self.add_simple_item(self.compare_results_list, "Brak danych do porównania.")
            self.set_status("Brak danych do porównania.")
            return

        for item in compare_result:
            title = item.get("title", "Bez tytułu")
            genre = item.get("genreName", "")
            owned_by_me = item.get("ownedByMe", False)
            owned_by_friend = item.get("ownedByFriend", False)
            my_collection = item.get("myCollectionName") or "-"
            friend_collection = item.get("friendCollectionName") or "-"

            self.add_compare_item(
                title,
                genre,
                owned_by_me,
                owned_by_friend,
                my_collection,
                friend_collection
            )

        self.set_status("Porównanie bibliotek gotowe.")

    def get_selected_search_result(self):
        selected_index = self.search_results_list.currentRow()

        if selected_index < 0 or not self.search_results:
            self.set_status("Wybierz użytkownika z listy.")
            return None

        if selected_index >= len(self.search_results):
            self.set_status("Wybierz poprawnego użytkownika z listy.")
            return None

        return self.search_results[selected_index]

    def get_selected_pending_request(self):
        selected_index = self.pending_list.currentRow()

        if selected_index < 0 or not self.pending_requests:
            self.set_status("Wybierz zaproszenie z listy.")
            return None

        if selected_index >= len(self.pending_requests):
            self.set_status("Wybierz poprawne zaproszenie z listy.")
            return None

        return self.pending_requests[selected_index]

    def get_selected_friend(self):
        selected_index = self.friends_list.currentRow()

        if selected_index < 0 or not self.friends:
            self.set_status("Wybierz znajomego z listy.")
            return None

        if selected_index >= len(self.friends):
            self.set_status("Wybierz poprawnego znajomego z listy.")
            return None

        return self.friends[selected_index]

    def set_status(self, message):
        self.status_label.setText(message)

    def handle_copy_invite_link(self):
        username = ""

        if hasattr(self, "current_user") and self.current_user:
            username = self.current_user.get("userName", "")

        invite_link = f"{WEB_REGISTER_URL}?invitedBy={username}"

        QApplication.clipboard().setText(invite_link)
        self.set_status("")

    def load_current_user(self):
        response = get_me()

        if response is not None and response.status_code == 200:
            self.current_user = response.json()
