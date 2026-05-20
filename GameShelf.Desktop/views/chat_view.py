from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox
)

from services.chat_service import (
    get_my_chats,
    get_chat_messages,
    create_chat
)
from services.chat_realtime_service import ChatRealtimeService
from services.friends_service import get_my_friends


class ChatView(QWidget):
    message_received = Signal(dict)

    def __init__(self):
        super().__init__()

        self.chats = []
        self.friends = []
        self.current_group_id = None
        self.realtime_service = ChatRealtimeService(
            self.emit_received_message
        )

        self.setup_ui()
        self.connect_signals()
        self.load_friends()
        self.load_chats()

        connected = self.realtime_service.connect()

        if not connected:
            self.set_status(
                "Czat w czasie rzeczywistym jest niedostępny. Historia rozmów nadal może działać."
            )

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Czat")

        create_layout = QVBoxLayout()

        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("Nazwa grupy opcjonalnie")

        self.friend_username_input = QLineEdit()
        self.friend_username_input.setPlaceholderText("Username znajomych po przecinku")

        self.create_button = QPushButton("Utwórz czat")

        create_layout.addWidget(QLabel("Nowa konwersacja"))
        create_layout.addWidget(self.group_name_input)
        create_layout.addWidget(self.friend_username_input)
        create_layout.addWidget(self.create_button)

        content_layout = QHBoxLayout()

        self.chats_list = QListWidget()
        self.messages_list = QListWidget()

        content_layout.addWidget(self.chats_list, 1)
        content_layout.addWidget(self.messages_list, 2)

        send_layout = QHBoxLayout()

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Napisz wiadomość...")
        self.message_input.setFixedHeight(80)

        self.send_button = QPushButton("Wyślij")

        send_layout.addWidget(self.message_input)
        send_layout.addWidget(self.send_button)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)

        layout.addWidget(title)
        layout.addLayout(create_layout)
        layout.addLayout(content_layout)
        layout.addLayout(send_layout)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def connect_signals(self):
        self.chats_list.currentRowChanged.connect(
            self.handle_chat_selected
        )
        self.send_button.clicked.connect(
            self.handle_send_message
        )
        self.create_button.clicked.connect(
            self.handle_create_chat
        )
        self.message_received.connect(
            self.add_received_message
        )

    def load_friends(self):
        self.friends = get_my_friends()

    def load_chats(self):
        self.chats_list.clear()
        self.messages_list.clear()

        self.chats = get_my_chats()

        if not self.chats:
            self.chats_list.addItem("Brak konwersacji")
            return

        for chat in self.chats:
            name = chat.get("name") or "Konwersacja"
            last_message = chat.get("lastMessage") or ""

            if last_message:
                self.chats_list.addItem(f"{name} — {last_message}")
            else:
                self.chats_list.addItem(name)

    def handle_chat_selected(self, index):
        if index < 0 or index >= len(self.chats):
            return

        chat = self.chats[index]
        group_id = chat.get("id")

        if not group_id:
            self.set_status("Nie udało się pobrać ID konwersacji.")
            return

        if self.current_group_id:
            self.realtime_service.unsubscribe(self.current_group_id)

        self.current_group_id = group_id
        self.realtime_service.subscribe(group_id)

        self.load_messages(group_id)

    def load_messages(self, group_id):
        self.messages_list.clear()

        messages = get_chat_messages(group_id)

        if not messages:
            self.messages_list.addItem("Brak wiadomości")
            return

        for message in messages:
            self.add_message_to_list(message)

    def handle_send_message(self):
        if not self.current_group_id:
            self.set_status("Wybierz konwersację.")
            return

        content = self.message_input.toPlainText().strip()

        if not content:
            self.set_status("Wpisz wiadomość.")
            return

        success = self.realtime_service.send_message(
            self.current_group_id,
            content
        )

        if not success:
            self.set_status("Nie udało się wysłać wiadomości.")
            return

        self.message_input.clear()

    def handle_create_chat(self):
        self.load_friends()

        group_name = self.group_name_input.text().strip()
        usernames_text = self.friend_username_input.text().strip()

        if not usernames_text:
            self.set_status("Podaj username znajomego.")
            return

        usernames = [
            username.strip()
            for username in usernames_text.split(",")
            if username.strip()
        ]

        user_ids, missing_usernames = self.get_friend_ids_by_usernames(usernames)

        if missing_usernames:
            self.set_status(
                f"Nie znaleziono znajomych: {', '.join(missing_usernames)}"
            )
            return

        if not user_ids:
            self.set_status("Nie znaleziono poprawnych znajomych.")
            return

        success, result = create_chat(
            group_name,
            user_ids
        )

        if not success:
            self.set_status(f"Nie udało się utworzyć czatu: {result}")
            return

        self.group_name_input.clear()
        self.friend_username_input.clear()
        self.set_status("Czat został utworzony.")
        self.load_chats()

    def get_friend_ids_by_usernames(self, usernames):
        user_ids = []
        missing_usernames = []

        friends_by_username = {}

        for friend in self.friends:
            username = friend.get("userName")

            if username:
                friends_by_username[username.lower()] = friend

        for username in usernames:
            friend = friends_by_username.get(username.lower())

            if not friend:
                missing_usernames.append(username)
                continue

            user_id = friend.get("userId") or friend.get("id")

            if not user_id:
                missing_usernames.append(username)
                continue

            user_ids.append(user_id)

        return user_ids, missing_usernames

    def emit_received_message(self, message):
        self.message_received.emit(message)

    def add_received_message(self, message):
        if message.get("groupId") != self.current_group_id:
            return

        self.add_message_to_list(message)

    def add_message_to_list(self, message):
        sender = message.get("senderName") or "Użytkownik"
        content = message.get("content") or ""
        timestamp = message.get("timestamp") or ""

        self.messages_list.addItem(
            f"{sender}: {content} ({timestamp})"
        )

    def set_status(self, message):
        self.status_label.setText(message)

    def closeEvent(self, event):
        self.realtime_service.stop()
        event.accept()