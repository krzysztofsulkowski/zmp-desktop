from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFrame,
    QScrollArea,
)

from services.chat_service import (
    get_my_chats,
    get_chat_messages,
    create_chat,
)
from services.chat_realtime_service import ChatRealtimeService
from services.friends_service import get_my_friends
from services.user_service import get_current_user
from components.chat_widgets import ChatListItemWidget, MessageBubbleWidget


class ChatView(QWidget):
    message_received = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setObjectName("chatView")

        self.chats = []
        self.friends = []
        self.current_group_id = None
        self.current_user = {}
        self.current_messages = []
        self.realtime_service = ChatRealtimeService(self.emit_received_message)

        self.setup_ui()
        self.connect_signals()
        self.load_current_user()
        self.load_friends()
        self.load_chats()
        self.connect_realtime()
        self.start_fallback_refresh()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(36, 28, 36, 28)
        main_layout.setSpacing(22)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(14)

        title_box = QVBoxLayout()
        title_box.setContentsMargins(0, 0, 0, 0)
        title_box.setSpacing(4)

        self.title_label = QLabel("Czat")
        self.title_label.setObjectName("chatPageTitle")

        self.subtitle_label = QLabel("Rozmawiaj ze znajomymi i grupami bez wychodzenia z aplikacji.")
        self.subtitle_label.setObjectName("chatPageSubtitle")
        self.subtitle_label.setWordWrap(True)

        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)

        self.refresh_button = QPushButton("Odśwież")
        self.refresh_button.setObjectName("chatSecondaryButton")
        self.refresh_button.setFixedWidth(118)

        header.addLayout(title_box, 1)
        header.addWidget(self.refresh_button, 0, Qt.AlignmentFlag.AlignTop)

        self.status_label = QLabel("")
        self.status_label.setObjectName("chatStatusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.hide()

        content = QHBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(18)

        self.left_card = QFrame()
        self.left_card.setObjectName("chatCard")
        self.left_card.setMinimumWidth(290)
        self.left_card.setMaximumWidth(340)

        left_layout = QVBoxLayout(self.left_card)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(14)

        conversations_title = QLabel("Konwersacje")
        conversations_title.setObjectName("chatSectionTitle")

        self.chats_list = QListWidget()
        self.chats_list.setObjectName("chatConversationsList")
        self.chats_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.chats_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        create_title = QLabel("Nowa konwersacja")
        create_title.setObjectName("chatSectionTitle")

        create_hint = QLabel("Wpisz username znajomego albo kilka nazw po przecinku. Nazwa grupy jest opcjonalna.")
        create_hint.setObjectName("chatHintLabel")
        create_hint.setWordWrap(True)

        self.group_name_input = QLineEdit()
        self.group_name_input.setObjectName("chatInput")
        self.group_name_input.setPlaceholderText("Nazwa grupy, np. Ekipa do rankedów")

        self.friend_username_input = QLineEdit()
        self.friend_username_input.setObjectName("chatInput")
        self.friend_username_input.setPlaceholderText("Username znajomych po przecinku")

        self.create_button = QPushButton("Utwórz czat")
        self.create_button.setObjectName("chatPrimaryButton")

        left_layout.addWidget(conversations_title)
        left_layout.addWidget(self.chats_list, 1)
        left_layout.addWidget(create_title)
        left_layout.addWidget(create_hint)
        left_layout.addWidget(self.group_name_input)
        left_layout.addWidget(self.friend_username_input)
        left_layout.addWidget(self.create_button)

        self.right_card = QFrame()
        self.right_card.setObjectName("chatCard")

        right_layout = QVBoxLayout(self.right_card)
        right_layout.setContentsMargins(20, 18, 20, 18)
        right_layout.setSpacing(14)

        self.conversation_title = QLabel("Wybierz konwersację")
        self.conversation_title.setObjectName("chatConversationTitle")
        self.conversation_title.setWordWrap(True)

        self.conversation_meta = QLabel("Po wybraniu rozmowy zobaczysz historię wiadomości.")
        self.conversation_meta.setObjectName("chatConversationMeta")
        self.conversation_meta.setWordWrap(True)

        self.messages_scroll = QScrollArea()
        self.messages_scroll.setObjectName("chatMessagesScrollArea")
        self.messages_scroll.setWidgetResizable(True)
        self.messages_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.messages_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.messages_widget = QWidget()
        self.messages_widget.setObjectName("chatMessagesWidget")
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(4, 8, 4, 8)
        self.messages_layout.setSpacing(10)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.empty_messages_label = QLabel("Nie wybrano żadnej konwersacji.")
        self.empty_messages_label.setObjectName("chatEmptyState")
        self.empty_messages_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_messages_label.setWordWrap(True)
        self.messages_layout.addWidget(self.empty_messages_label, 1)

        self.messages_scroll.setWidget(self.messages_widget)

        send_layout = QHBoxLayout()
        send_layout.setContentsMargins(0, 0, 0, 0)
        send_layout.setSpacing(12)

        self.message_input = QTextEdit()
        self.message_input.setObjectName("chatMessageInput")
        self.message_input.setPlaceholderText("Napisz wiadomość...")
        self.message_input.setFixedHeight(76)

        self.send_button = QPushButton("Wyślij")
        self.send_button.setObjectName("chatPrimaryButton")
        self.send_button.setFixedWidth(118)
        self.send_button.setFixedHeight(76)
        self.send_button.setEnabled(False)

        send_layout.addWidget(self.message_input, 1)
        send_layout.addWidget(self.send_button)

        right_layout.addWidget(self.conversation_title)
        right_layout.addWidget(self.conversation_meta)
        right_layout.addWidget(self.messages_scroll, 1)
        right_layout.addLayout(send_layout)

        content.addWidget(self.left_card)
        content.addWidget(self.right_card, 1)

        main_layout.addLayout(header)
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(content, 1)

    def connect_signals(self):
        self.chats_list.currentRowChanged.connect(self.handle_chat_selected)
        self.send_button.clicked.connect(self.handle_send_message)
        self.create_button.clicked.connect(self.handle_create_chat)
        self.refresh_button.clicked.connect(self.handle_refresh)
        self.message_received.connect(self.add_received_message)

    def load_current_user(self):
        self.current_user = get_current_user()

    def connect_realtime(self):
        connected = self.realtime_service.connect()

        if connected:
            self.set_status("Połączono z czatem w czasie rzeczywistym.", temporary=True)
            return

        self.set_status("Czat real-time jest chwilowo niedostępny. Historia rozmów i odświeżanie nadal działają.")

    def start_fallback_refresh(self):
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(12000)
        self.refresh_timer.timeout.connect(self.refresh_current_chat_if_needed)
        self.refresh_timer.start()

    def load_friends(self):
        self.friends = get_my_friends()

    def load_chats(self, select_group_id=None):
        previous_group_id = select_group_id or self.current_group_id
        self.chats_list.clear()
        self.chats = get_my_chats()

        if not self.chats:
            item = QListWidgetItem("Brak konwersacji")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.chats_list.addItem(item)
            self.show_empty_messages("Nie masz jeszcze żadnej konwersacji. Utwórz czat z lewej strony.")
            self.send_button.setEnabled(False)
            return

        selected_row = 0

        for index, chat in enumerate(self.chats):
            if previous_group_id and chat.get("id") == previous_group_id:
                selected_row = index

            item = QListWidgetItem()
            item.setSizeHint(item.sizeHint().expandedTo(item.sizeHint()))
            self.chats_list.addItem(item)
            widget = ChatListItemWidget(
                self.get_chat_name(chat),
                self.get_participants_text(chat),
                chat.get("lastMessage") or "",
                chat.get("lastMessageTime"),
            )
            item.setSizeHint(widget.sizeHint())
            self.chats_list.setItemWidget(item, widget)

        self.chats_list.setCurrentRow(selected_row)

    def handle_chat_selected(self, index):
        if index < 0 or index >= len(self.chats):
            return

        chat = self.chats[index]
        group_id = chat.get("id")

        if not group_id:
            self.set_status("Nie udało się pobrać ID konwersacji.")
            return

        if self.current_group_id and self.current_group_id != group_id:
            self.realtime_service.unsubscribe(self.current_group_id)

        self.current_group_id = group_id
        self.realtime_service.subscribe(group_id)
        self.conversation_title.setText(self.get_chat_name(chat))
        self.conversation_meta.setText(self.get_participants_text(chat))
        self.send_button.setEnabled(True)
        self.load_messages(group_id)

    def load_messages(self, group_id):
        messages = get_chat_messages(group_id)
        self.current_messages = messages
        self.clear_messages()

        if not messages:
            self.show_empty_messages("W tej konwersacji nie ma jeszcze wiadomości. Napisz pierwszą.")
            return

        for message in messages:
            self.add_message_to_layout(message)

        self.scroll_messages_to_bottom()

    def handle_send_message(self):
        if not self.current_group_id:
            self.set_status("Najpierw wybierz konwersację.")
            return

        content = self.message_input.toPlainText().strip()

        if not content:
            self.set_status("Wpisz treść wiadomości.")
            return

        success = self.realtime_service.send_message(self.current_group_id, content)

        if not success:
            self.set_status("Nie udało się wysłać wiadomości przez real-time. Sprawdź połączenie z API i hubem SignalR.")
            return

        self.message_input.clear()

    def handle_create_chat(self):
        self.load_friends()

        group_name = self.group_name_input.text().strip()
        usernames_text = self.friend_username_input.text().strip()

        if not usernames_text:
            self.set_status("Podaj username znajomego albo kilka username'ów po przecinku.")
            return

        usernames = [username.strip() for username in usernames_text.split(",") if username.strip()]
        user_ids, missing_usernames = self.get_friend_ids_by_usernames(usernames)

        if missing_usernames:
            self.set_status(f"Nie znaleziono tych znajomych: {', '.join(missing_usernames)}.")
            return

        if not user_ids:
            self.set_status("Nie znaleziono poprawnych znajomych do dodania.")
            return

        success, result = create_chat(group_name, user_ids)

        if not success:
            self.set_status(f"Nie udało się utworzyć czatu: {result}")
            return

        self.group_name_input.clear()
        self.friend_username_input.clear()
        self.set_status("Czat został utworzony.", temporary=True)
        self.load_chats(select_group_id=result if isinstance(result, int) else None)

    def get_friend_ids_by_usernames(self, usernames):
        user_ids = []
        missing_usernames = []
        friends_by_username = {}

        for friend in self.friends:
            username = friend.get("userName") or friend.get("username")

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

    def handle_refresh(self):
        self.load_chats(select_group_id=self.current_group_id)
        self.set_status("Odświeżono czat.", temporary=True)

    def refresh_current_chat_if_needed(self):
        if self.current_group_id and not self.realtime_service.is_connected:
            self.load_messages(self.current_group_id)

    def emit_received_message(self, message):
        self.message_received.emit(message)

    def add_received_message(self, message):
        if int(message.get("groupId") or 0) != int(self.current_group_id or 0):
            return

        self.add_message_to_layout(message)
        self.current_messages.append(message)
        self.scroll_messages_to_bottom()

    def add_message_to_layout(self, message):
        if self.empty_messages_label:
            self.empty_messages_label.hide()

        sender = message.get("senderName") or "Użytkownik"
        content = message.get("content") or ""
        timestamp = message.get("timestamp") or message.get("Timestamp") or ""
        is_own = self.is_own_message(message)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        bubble = MessageBubbleWidget(sender, content, timestamp, is_own)

        if is_own:
            row.addStretch(1)
            row.addWidget(bubble)
        else:
            row.addWidget(bubble)
            row.addStretch(1)

        self.messages_layout.addLayout(row)

    def is_own_message(self, message):
        sender_id = str(message.get("senderId") or "")
        sender_name = str(message.get("senderName") or "").lower()
        current_id = str(self.current_user.get("id") or self.current_user.get("userId") or "")
        current_name = str(self.current_user.get("userName") or self.current_user.get("username") or "").lower()

        if current_id and sender_id and current_id == sender_id:
            return True

        return bool(current_name and sender_name and current_name == sender_name)

    def clear_messages(self):
        while self.messages_layout.count():
            item = self.messages_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

            child_layout = item.layout()

            if child_layout:
                while child_layout.count():
                    child_item = child_layout.takeAt(0)
                    child_widget = child_item.widget()

                    if child_widget:
                        child_widget.deleteLater()

        self.empty_messages_label = None

    def show_empty_messages(self, text):
        self.clear_messages()
        self.empty_messages_label = QLabel(text)
        self.empty_messages_label.setObjectName("chatEmptyState")
        self.empty_messages_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_messages_label.setWordWrap(True)
        self.messages_layout.addWidget(self.empty_messages_label, 1)

    def scroll_messages_to_bottom(self):
        QTimer.singleShot(0, lambda: self.messages_scroll.verticalScrollBar().setValue(self.messages_scroll.verticalScrollBar().maximum()))

    def get_chat_name(self, chat):
        name = chat.get("name")

        if name:
            return name

        participants = chat.get("participants") or []

        if participants:
            return ", ".join(participants[:3])

        return "Konwersacja"

    def get_participants_text(self, chat):
        participants = chat.get("participants") or []

        if not participants:
            return "Brak danych o uczestnikach"

        if len(participants) <= 3:
            return "Uczestnicy: " + ", ".join(participants)

        return "Uczestnicy: " + ", ".join(participants[:3]) + f" +{len(participants) - 3}"

    def set_status(self, message, temporary=False):
        self.status_label.setText(message)
        self.status_label.setVisible(bool(message))

        if temporary:
            QTimer.singleShot(3500, lambda: self.status_label.hide())

    def closeEvent(self, event):
        self.realtime_service.stop()
        event.accept()
