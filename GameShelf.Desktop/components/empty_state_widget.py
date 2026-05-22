from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class EmptyStateWidget(QLabel):
    def __init__(self, text=""):
        super().__init__(text)

        self.setObjectName("emptyState")
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
