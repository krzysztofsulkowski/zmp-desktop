from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class FriendsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Friends view")

        layout.addWidget(label)
        self.setLayout(layout)