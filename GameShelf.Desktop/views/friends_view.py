from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QLineEdit,
    QPushButton,
    QApplication
)

from config import WEB_REGISTER_URL

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

        self.setup_ui()
        self.connect_signals()
        self.load_friends()
        self.load_pending_requests()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Znajomi")

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Wpisz nazwę użytkownika")

        self.search_button = QPushButton("Szukaj")
        self.add_button = QPushButton("Dodaj wybranego")

        self.invite_link_button = QPushButton("Kopiuj link zaproszenia")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.add_button)

        self.results_label = QLabel("Wyniki wyszukiwania")
        self.search_results_list = QListWidget()

        self.pending_label = QLabel("Zaproszenia oczekujące")
        self.pending_list = QListWidget()

        pending_buttons_layout = QHBoxLayout()

        self.accept_button = QPushButton("Akceptuj wybrane")
        self.reject_button = QPushButton("Odrzuć wybrane")

        pending_buttons_layout.addWidget(self.accept_button)
        pending_buttons_layout.addWidget(self.reject_button)

        self.friends_label = QLabel("Twoi znajomi")
        self.friends_list = QListWidget()

        friend_buttons_layout = QHBoxLayout()

        self.view_collections_button = QPushButton("Pokaż kolekcje")
        self.compare_button = QPushButton("Porównaj biblioteki")
        self.remove_friend_button = QPushButton("Usuń znajomego")

        friend_buttons_layout.addWidget(self.view_collections_button)
        friend_buttons_layout.addWidget(self.compare_button)
        friend_buttons_layout.addWidget(self.remove_friend_button)
        friend_buttons_layout.addWidget(self.invite_link_button)

        self.friend_collections_label = QLabel("Kolekcje znajomego")
        self.friend_collections_list = QListWidget()

        self.compare_results_label = QLabel("Porównanie bibliotek")
        self.compare_results_list = QListWidget()

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)

        layout.addWidget(title)
        layout.addLayout(search_layout)
        layout.addWidget(self.results_label)
        layout.addWidget(self.search_results_list)
        layout.addWidget(self.pending_label)
        layout.addWidget(self.pending_list)
        layout.addLayout(pending_buttons_layout)
        layout.addWidget(self.friends_label)
        layout.addWidget(self.friends_list)
        layout.addLayout(friend_buttons_layout)
        layout.addWidget(self.friend_collections_label)
        layout.addWidget(self.friend_collections_list)
        layout.addWidget(self.compare_results_label)
        layout.addWidget(self.compare_results_list)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def connect_signals(self):
        self.search_button.clicked.connect(self.handle_search)
        self.add_button.clicked.connect(self.handle_add_selected_friend)
        self.accept_button.clicked.connect(self.handle_accept_selected_request)
        self.reject_button.clicked.connect(self.handle_reject_selected_request)
        self.view_collections_button.clicked.connect(self.handle_view_friend_collections)
        self.compare_button.clicked.connect(self.handle_compare_friend)
        self.remove_friend_button.clicked.connect(self.handle_remove_selected_friend)
        self.invite_link_button.clicked.connect(
            self.handle_copy_invite_link
        )

    def load_friends(self):
        self.friends_list.clear()
        self.friend_collections_list.clear()
        self.compare_results_list.clear()

        self.friends = get_my_friends()

        if not self.friends:
            self.friends_list.addItem("Brak znajomych")
            return

        for friend in self.friends:
            username = friend.get("userName", "Nieznany użytkownik")
            self.friends_list.addItem(username)

    def load_pending_requests(self):
        self.pending_list.clear()

        self.pending_requests = get_pending_requests()

        if not self.pending_requests:
            self.pending_list.addItem("Brak zaproszeń")
            return

        for request in self.pending_requests:
            username = request.get("userName", "Nieznany użytkownik")
            self.pending_list.addItem(username)

    def handle_search(self):
        search_value = self.search_input.text().strip()

        if not search_value:
            self.set_status("Wpisz nazwę użytkownika.")
            return

        self.search_results = search_users(search_value)
        self.search_results_list.clear()

        if not self.search_results:
            self.search_results_list.addItem("Brak wyników")
            self.set_status("Nie znaleziono użytkowników.")
            return

        for user in self.search_results:
            username = user.get("userName", "Nieznany użytkownik")
            email = user.get("email")

            if email:
                self.search_results_list.addItem(f"{username} ({email})")
            else:
                self.search_results_list.addItem(username)

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
            self.friend_collections_list.addItem("Brak publicznych kolekcji")
            self.set_status("Znajomy nie ma publicznych kolekcji.")
            return

        for collection in collections:
            collection_name = collection.get("collectionName", "Bez nazwy")
            games = collection.get("games", [])

            self.friend_collections_list.addItem(
                f"{collection_name} ({len(games)} gier)"
            )

            for game in games:
                title = game.get("title", "Bez tytułu")
                self.friend_collections_list.addItem(f"  - {title}")

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
            self.compare_results_list.addItem("Brak danych do porównania.")
            self.set_status("Brak danych do porównania.")
            return

        for item in compare_result:
            title = item.get("title", "Bez tytułu")
            genre = item.get("genreName", "")
            owned_by_me = item.get("ownedByMe", False)
            owned_by_friend = item.get("ownedByFriend", False)
            my_collection = item.get("myCollectionName") or "-"
            friend_collection = item.get("friendCollectionName") or "-"

            ownership = []

            if owned_by_me:
                ownership.append(f"u mnie: {my_collection}")

            if owned_by_friend:
                ownership.append(f"u znajomego: {friend_collection}")

            ownership_text = ", ".join(ownership) or "brak danych"

            self.compare_results_list.addItem(
                f"{title} ({genre}) — {ownership_text}"
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
        QApplication.clipboard().setText(
            WEB_REGISTER_URL
        )

        self.set_status(
            "Link zaproszenia został skopiowany do schowka."
        )