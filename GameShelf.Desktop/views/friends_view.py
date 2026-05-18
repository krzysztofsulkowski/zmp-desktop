from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QLineEdit,
    QPushButton
)

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

        self.search_results = []
        self.pending_requests = []
        self.friends = []

        layout = QVBoxLayout()

        title = QLabel("Znajomi")

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Wpisz nazwę użytkownika")

        self.search_button = QPushButton("Search")
        self.add_button = QPushButton("Add selected")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.add_button)

        self.results_label = QLabel("Wyniki wyszukiwania")
        self.search_results_list = QListWidget()

        self.pending_label = QLabel("Zaproszenia oczekujące")
        self.pending_list = QListWidget()

        pending_buttons_layout = QHBoxLayout()

        self.accept_button = QPushButton("Accept selected")
        self.reject_button = QPushButton("Reject selected")

        pending_buttons_layout.addWidget(self.accept_button)
        pending_buttons_layout.addWidget(self.reject_button)

        self.friends_label = QLabel("Twoi znajomi")
        self.friends_list = QListWidget()

        self.friend_collections_label = QLabel("Kolekcje znajomego")
        self.friend_collections_list = QListWidget()

        self.compare_results_label = QLabel("Porównanie bibliotek")
        self.compare_results_list = QListWidget()

        self.view_collections_button = QPushButton("View selected collections")

        self.compare_button = QPushButton("Compare selected")

        self.status_label = QLabel("")

        layout.addWidget(title)
        layout.addLayout(search_layout)
        layout.addWidget(self.results_label)
        layout.addWidget(self.search_results_list)
        layout.addWidget(self.pending_label)
        layout.addWidget(self.pending_list)
        layout.addLayout(pending_buttons_layout)
        layout.addWidget(self.friends_label)
        layout.addWidget(self.friends_list)
        layout.addWidget(self.view_collections_button)
        layout.addWidget(self.compare_button)
        layout.addWidget(self.friend_collections_label)
        layout.addWidget(self.friend_collections_list)
        layout.addWidget(self.compare_results_label)
        layout.addWidget(self.compare_results_list)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.search_button.clicked.connect(self.handle_search)
        self.add_button.clicked.connect(self.handle_add_selected_friend)
        self.accept_button.clicked.connect(self.handle_accept_selected_request)
        self.reject_button.clicked.connect(self.handle_reject_selected_request)
        self.view_collections_button.clicked.connect(self.handle_view_friend_collections)
        self.compare_button.clicked.connect(self.handle_compare_friend)

        self.load_friends()
        self.load_pending_requests()

    def load_friends(self):
        self.friends_list.clear()

        self.friends = get_my_friends()

        if not self.friends:
            self.friends_list.addItem("Brak znajomych")
            return

        for friend in self.friends:
            username = friend.get("userName", "Unknown")
            self.friends_list.addItem(username)

    def load_pending_requests(self):
        self.pending_list.clear()

        self.pending_requests = get_pending_requests()

        if not self.pending_requests:
            self.pending_list.addItem("Brak zaproszeń")
            return

        for request in self.pending_requests:
            print("PENDING REQUEST OBJECT:", request)
            username = request.get("userName", "Unknown")
            self.pending_list.addItem(username)

    def handle_search(self):
        search_value = self.search_input.text().strip()

        if not search_value:
            self.status_label.setText("Wpisz nazwę użytkownika.")
            return

        self.search_results = search_users(search_value)
        self.search_results_list.clear()

        if not self.search_results:
            self.search_results_list.addItem("Brak wyników")
            return

        for user in self.search_results:
            username = user.get("userName", "Unknown")
            email = user.get("email", "")

            if email:
                self.search_results_list.addItem(f"{username} ({email})")
            else:
                self.search_results_list.addItem(username)

    def handle_add_selected_friend(self):
        selected_index = self.search_results_list.currentRow()

        if selected_index < 0:
            self.status_label.setText("Wybierz użytkownika z listy.")
            return

        if not self.search_results:
            self.status_label.setText("Brak użytkownika do dodania.")
            return

        selected_user = self.search_results[selected_index]
        username = selected_user.get("userName")

        if not username:
            self.status_label.setText("Nie udało się pobrać nazwy użytkownika.")
            return

        success, message = add_friend_by_username(username)
        self.status_label.setText(message)

        if success:
            self.load_pending_requests()
            self.load_friends()

    def handle_accept_selected_request(self):
        selected_index = self.pending_list.currentRow()

        if selected_index < 0:
            self.status_label.setText("Wybierz zaproszenie z listy.")
            return

        if not self.pending_requests:
            self.status_label.setText("Brak zaproszenia do zaakceptowania.")
            return

        selected_request = self.pending_requests[selected_index]
        requester_id = selected_request.get("userId")

        if not requester_id:
            self.status_label.setText("Nie udało się pobrać ID zapraszającego.")
            return

        success, message = accept_friend_request(requester_id)
        self.status_label.setText(message)

        if success:
            self.load_pending_requests()
            self.load_friends()

    def handle_reject_selected_request(self):
        selected_index = self.pending_list.currentRow()

        if selected_index < 0:
            self.status_label.setText("Wybierz zaproszenie z listy.")
            return

        if not self.pending_requests:
            self.status_label.setText("Brak zaproszenia do odrzucenia.")
            return

        selected_request = self.pending_requests[selected_index]
        requester_id = selected_request.get("userId")

        if not requester_id:
            self.status_label.setText("Nie udało się pobrać ID zapraszającego.")
            return

        success, message = reject_or_remove_friend(requester_id)
        self.status_label.setText(message)

        if success:
            self.load_pending_requests()
            self.load_friends()

    def handle_view_friend_collections(self):
        selected_index = self.friends_list.currentRow()

        if selected_index < 0:
            self.status_label.setText("Wybierz znajomego z listy.")
            return

        if not self.friends:
            self.status_label.setText("Brak znajomego do podglądu.")
            return

        selected_friend = self.friends[selected_index]
        friend_id = selected_friend.get("userId") or selected_friend.get("id")

        if not friend_id:
            self.status_label.setText("Nie udało się pobrać ID znajomego.")
            return

        collections = get_friend_collections_with_games(friend_id)

        self.friend_collections_list.clear()

        if not collections:
            self.friend_collections_list.addItem("Brak publicznych kolekcji")
            return

        for collection in collections:
            collection_name = collection.get("collectionName", "Bez nazwy")
            games = collection.get("games", [])

            self.friend_collections_list.addItem(f"{collection_name} ({len(games)} gier)")

            for game in games:
                title = game.get("title", "Bez tytułu")
                self.friend_collections_list.addItem(f"  - {title}")

        self.status_label.setText("Kolekcje znajomego pobrane.")

    def handle_compare_friend(self):
        selected_index = self.friends_list.currentRow()

        if selected_index < 0:
            self.status_label.setText("Wybierz znajomego.")
            return

        selected_friend = self.friends[selected_index]
        friend_id = selected_friend.get("userId") or selected_friend.get("id")

        if not friend_id:
            self.status_label.setText("Nie udało się pobrać ID znajomego.")
            return

        compare_result = compare_with_friend(friend_id)

        print("COMPARE RESULT:", compare_result)

        self.compare_results_list.clear()

        if not compare_result:
            self.compare_results_list.addItem("Brak danych do porównania.")
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

            ownership_text = ", ".join(ownership)

            self.compare_results_list.addItem(
                f"{title} ({genre}) — {ownership_text}"
            )

        self.status_label.setText("Porównanie bibliotek gotowe.")