from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout

from utils.datetime_formatter import format_datetime


class ChatListItemWidget(QFrame):
    def __init__(self, name, participants, last_message, last_message_time):
        super().__init__()
        self.setObjectName("chatListItem")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(5)

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(8)

        title = QLabel(name)
        title.setObjectName("chatListItemTitle")
        title.setWordWrap(True)

        time_label = QLabel(format_datetime(last_message_time, compact=True))
        time_label.setObjectName("chatListItemTime")
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        time_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

        title_row.addWidget(title, 1)
        title_row.addWidget(time_label)

        members = QLabel(participants)
        members.setObjectName("chatListItemMeta")
        members.setWordWrap(True)

        preview_text = last_message if last_message else "Brak wiadomości w tej konwersacji"
        preview = QLabel(preview_text)
        preview.setObjectName("chatListItemPreview")
        preview.setWordWrap(True)

        layout.addLayout(title_row)
        layout.addWidget(members)
        layout.addWidget(preview)


class MessageBubbleWidget(QFrame):
    def __init__(self, sender, content, timestamp, is_own):
        super().__init__()
        self.setObjectName("messageBubbleOwn" if is_own else "messageBubbleOther")
        self.setMaximumWidth(560)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(6)

        header = QLabel(f"{sender} • {format_datetime(timestamp)}")
        header.setObjectName("messageHeaderOwn" if is_own else "messageHeaderOther")
        header.setWordWrap(True)

        body = QLabel(content)
        body.setObjectName("messageBodyOwn" if is_own else "messageBodyOther")
        body.setWordWrap(True)
        body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addWidget(header)
        layout.addWidget(body)
