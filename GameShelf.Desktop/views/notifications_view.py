from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class NotificationsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Notifications view")

        layout.addWidget(label)
        self.setLayout(layout)