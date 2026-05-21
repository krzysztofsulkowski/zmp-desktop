from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from utils.window_corners import disable_windows_11_rounded_corners


class DraggableFramelessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_position = QPoint()
        self._is_dragging = False
        self._drag_widgets = []

    def _register_drag_widget(self, widget):
        widget.installEventFilter(self)
        self._drag_widgets.append(widget)

    def _start_drag(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return False

        self._is_dragging = True
        self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        event.accept()
        return True

    def _move_dragged_window(self, event):
        if not self._is_dragging or not event.buttons() == Qt.MouseButton.LeftButton:
            return False

        self.move(event.globalPosition().toPoint() - self._drag_position)
        event.accept()
        return True

    def eventFilter(self, watched, event):
        if watched in self._drag_widgets:
            if event.type() == QEvent.Type.MouseButtonPress:
                return self._start_drag(event)
            if event.type() == QEvent.Type.MouseMove:
                return self._move_dragged_window(event)
            if event.type() == QEvent.Type.MouseButtonRelease:
                self._is_dragging = False
                event.accept()
                return True

        return super().eventFilter(watched, event)

    def mousePressEvent(self, event):
        if self._start_drag(event):
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._move_dragged_window(event):
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._is_dragging = False
        event.accept()
        super().mouseReleaseEvent(event)


class StyledDialog(DraggableFramelessDialog):
    def __init__(self, title, parent=None, show_close=True):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.dialog_frame = QFrame()
        self.dialog_frame.setObjectName("styledDialogFrame")

        frame_layout = QVBoxLayout(self.dialog_frame)
        frame_layout.setContentsMargins(22, 18, 22, 22)
        frame_layout.setSpacing(16)

        self.header = QWidget()
        self.header.setObjectName("styledDialogHeader")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("styledDialogTitle")

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        if show_close:
            self.close_button = QPushButton("×")
            self.close_button.setObjectName("styledDialogCloseButton")
            self.close_button.setFixedSize(34, 34)
            self.close_button.clicked.connect(self.reject)
            header_layout.addWidget(self.close_button)
        else:
            self.close_button = None

        frame_layout.addWidget(self.header)

        self.body = QWidget()
        self.body.setObjectName("styledDialogBody")
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(12)
        frame_layout.addWidget(self.body)

        root_layout.addWidget(self.dialog_frame)

        self._register_drag_widget(self.header)
        self._register_drag_widget(self.title_label)

    def showEvent(self, event):
        super().showEvent(event)
        disable_windows_11_rounded_corners(self)


class StyledMessageDialog(DraggableFramelessDialog):
    def __init__(self, title, message, kind="info", buttons=None, parent=None):
        super().__init__(parent)

        self.clicked_role = None
        self.setWindowTitle(title or "GameShelf")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)
        self.setMinimumWidth(330)

        if buttons is None:
            buttons = [("OK", "ok")]

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setObjectName("styledMessageFrame")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(22, 18, 22, 18)
        frame_layout.setSpacing(16)

        self.header = QWidget()
        self.header.setObjectName("styledDialogHeader")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = None
        display_title = "" if title == "GameShelf" else title

        if display_title:
            self.title_label = QLabel(display_title)
            self.title_label.setObjectName("styledMessageTitle")
            header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        close_button = QPushButton("×")
        close_button.setObjectName("styledDialogCloseButton")
        close_button.setFixedSize(32, 32)
        close_button.clicked.connect(self.reject)
        header_layout.addWidget(close_button)
        frame_layout.addWidget(self.header)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)

        icon_label = QLabel("!" if kind == "warning" else "?")
        icon_label.setObjectName("styledMessageWarningIcon" if kind == "warning" else "styledMessageInfoIcon")
        icon_label.setFixedSize(34, 34)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)

        message_label = QLabel(message)
        message_label.setObjectName("styledMessageText")
        message_label.setWordWrap(True)
        content_layout.addWidget(message_label, 1)
        frame_layout.addLayout(content_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        for text, role in buttons:
            button = QPushButton(text)
            button.setObjectName("styledMessageButton")
            button.clicked.connect(lambda checked=False, selected_role=role: self._finish(selected_role))
            buttons_layout.addWidget(button)

        frame_layout.addLayout(buttons_layout)
        root_layout.addWidget(frame)

        self._register_drag_widget(self.header)
        if self.title_label is not None:
            self._register_drag_widget(self.title_label)

    def _finish(self, role):
        self.clicked_role = role
        self.accept()

    def showEvent(self, event):
        super().showEvent(event)
        disable_windows_11_rounded_corners(self)


def show_info(parent, message, title=""):
    dialog = StyledMessageDialog(title, message, "info", [("OK", "ok")], parent)
    dialog.exec()


def show_warning(parent, message, title=""):
    dialog = StyledMessageDialog(title, message, "warning", [("OK", "ok")], parent)
    dialog.exec()


def ask_confirmation(parent, message, title=""):
    dialog = StyledMessageDialog(title, message, "info", [("Tak", "yes"), ("Nie", "no")], parent)
    result = dialog.exec()
    return result == QDialog.DialogCode.Accepted and dialog.clicked_role == "yes"
