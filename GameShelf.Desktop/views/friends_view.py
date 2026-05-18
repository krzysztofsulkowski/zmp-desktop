from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget
)

from services.friends_service import get_my_friends


class FriendsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Znajomi")

        self.friends_list = QListWidget()

        layout.addWidget(title)
        layout.addWidget(self.friends_list)

        self.setLayout(layout)

        self.load_friends()

    def load_friends(self):
        self.friends_list.clear()

        friends = get_my_friends()

        if not friends:
            self.friends_list.addItem("Brak znajomych")
            return

        for friend in friends:
            username = friend.get("userName", "Unknown")
            self.friends_list.addItem(username)