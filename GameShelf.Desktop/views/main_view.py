from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MainView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GameShelf")

        layout = QVBoxLayout()

        self.label = QLabel("You are logged in!")

        layout.addWidget(self.label)

        self.setLayout(layout)