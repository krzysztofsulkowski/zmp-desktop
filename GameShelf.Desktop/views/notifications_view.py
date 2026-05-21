import json
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QSizePolicy
)

from services.friends_service import get_pending_requests


class NotificationCard(QFrame):
    def __init__(self, notification_id, title, content, is_unread, on_toggle):
        super().__init__()

        self.notification_id = notification_id
        self.on_toggle = on_toggle
        self.is_unread = is_unread

        self.setObjectName("notificationCard")
        self.setProperty("unread", is_unread)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("notificationCardTitle")
        self.title_label.setWordWrap(True)

        self.content_label = QLabel(content)
        self.content_label.setObjectName("notificationCardContent")
        self.content_label.setWordWrap(True)

        self.status_label = QLabel()
        self.status_label.setObjectName("notificationStatus")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.title_label)
        layout.addWidget(self.content_label)
        layout.addWidget(self.status_label)

        self.refresh_state()

    def refresh_state(self):
        self.setProperty("unread", self.is_unread)
        self.status_label.setText("Nowe" if self.is_unread else "Przeczytane")
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_unread = not self.is_unread
            self.refresh_state()
            self.on_toggle(self.notification_id, self.is_unread)

        super().mousePressEvent(event)


class NotificationsView(QWidget):
    unread_count_changed = Signal(int)

    def __init__(self):
        super().__init__()

        self.setObjectName("notificationsView")
        self.storage_path = Path(__file__).resolve().parents[1] / "notifications_read.json"
        self.read_notifications = self.load_read_notifications()
        self.session_read_notifications = set()
        self.notifications = []

        self.setup_ui()
        self.refresh_notifications()

    def setup_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(42, 24, 42, 32)
        root_layout.setSpacing(22)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("Powiadomienia")
        self.title_label.setObjectName("notificationsPageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mark_all_button = QPushButton("Zaznacz wszystko jako przeczytane")
        self.mark_all_button.setObjectName("markAllNotificationsButton")
        self.mark_all_button.clicked.connect(self.mark_all_as_read)

        header_layout.addStretch()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.mark_all_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("notificationsScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("notificationsScrollWidget")

        self.notifications_layout = QVBoxLayout(self.scroll_widget)
        self.notifications_layout.setContentsMargins(0, 0, 18, 24)
        self.notifications_layout.setSpacing(16)
        self.notifications_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_widget)

        root_layout.addLayout(header_layout)
        root_layout.addWidget(self.scroll_area, 1)

    def load_read_notifications(self):
        if not self.storage_path.exists():
            return set()

        try:
            with open(self.storage_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception:
            return set()

        if not isinstance(data, list):
            return set()

        return set(data)

    def save_read_notifications(self):
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(sorted(self.read_notifications), file, ensure_ascii=False, indent=2)

    def clear_layout(self):
        while self.notifications_layout.count():
            item = self.notifications_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

    def refresh_notifications(self):
        pending_requests = get_pending_requests()
        self.notifications = []

        for request in pending_requests:
            username = request.get("userName") or request.get("username") or "Nieznany użytkownik"
            user_id = request.get("userId") or request.get("id") or username
            notification_id = f"friend_request:{user_id}"

            self.notifications.append({
                "id": notification_id,
                "title": "Zaproszenie do znajomych",
                "content": f"Użytkownik {username} wysłał Ci zaproszenie do znajomych."
            })

        self.render_notifications()
        self.emit_unread_count()

    def render_notifications(self):
        self.clear_layout()
        visible_notifications = self.get_visible_notifications()

        if not visible_notifications:
            empty_card = QFrame()
            empty_card.setObjectName("emptyNotificationsCard")

            layout = QVBoxLayout(empty_card)
            layout.setContentsMargins(22, 22, 22, 22)

            label = QLabel("Brak powiadomień")
            label.setObjectName("emptyNotificationsLabel")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout.addWidget(label)

            self.notifications_layout.addWidget(empty_card)
            self.notifications_layout.addStretch()
            return

        for notification in visible_notifications:
            notification_id = notification["id"]
            is_unread = notification_id not in self.read_notifications

            card = NotificationCard(
                notification_id,
                notification["title"],
                notification["content"],
                is_unread,
                self.toggle_notification_state
            )
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            self.notifications_layout.addWidget(card)

        self.notifications_layout.addStretch()

    def get_visible_notifications(self):
        return [
            notification
            for notification in self.notifications
            if notification["id"] not in self.read_notifications or notification["id"] in self.session_read_notifications
        ]

    def toggle_notification_state(self, notification_id, is_unread):
        if is_unread:
            self.read_notifications.discard(notification_id)
            self.session_read_notifications.discard(notification_id)
        else:
            self.read_notifications.add(notification_id)
            self.session_read_notifications.add(notification_id)

        self.save_read_notifications()
        self.emit_unread_count()

    def mark_all_as_read(self):
        for notification in self.notifications:
            self.read_notifications.add(notification["id"])
            self.session_read_notifications.add(notification["id"])

        self.save_read_notifications()
        self.render_notifications()
        self.emit_unread_count()

    def get_unread_count(self):
        return len([
            notification
            for notification in self.notifications
            if notification["id"] not in self.read_notifications
        ])

    def emit_unread_count(self):
        self.unread_count_changed.emit(self.get_unread_count())

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_notifications()
