from pathlib import Path

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame


class DialogShell(QDialog):
    def __init__(self, title, width=500, height=None, parent=None):
        super().__init__(parent)

        self.base_dir = Path(__file__).resolve().parents[1]
        self.drag_position = QPoint()
        self.is_dragging = False

        self.setWindowTitle(title)
        self.setObjectName("popupDialog")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)
        self.setMinimumWidth(width)

        if height:
            self.setMinimumHeight(height)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("popupDialogFrame")

        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(22, 18, 22, 22)
        frame_layout.setSpacing(14)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 4)
        header_layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("popupDialogTitle")

        self.close_button = QPushButton()
        self.close_button.setObjectName("popupDialogCloseButton")
        self.close_button.setIcon(QIcon(str(self.base_dir / "assets" / "WindowCloseIcon.svg")))
        self.close_button.setFixedSize(34, 34)
        self.close_button.clicked.connect(self.reject)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_button)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        frame_layout.addLayout(header_layout)
        frame_layout.addLayout(self.content_layout)
        outer_layout.addWidget(self.frame)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        event.accept()
