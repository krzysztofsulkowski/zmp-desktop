from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class GlobalStatsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Global Stats view")

        layout.addWidget(label)
        self.setLayout(layout)