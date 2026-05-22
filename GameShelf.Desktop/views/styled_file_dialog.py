from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QPainterPath, QPixmap, QRegion
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QPushButton, QWidget

from utils.app_identity import get_window_title
from utils.window_corners import disable_windows_11_rounded_corners


class StyledFileDialog(QFileDialog):
    def __init__(self, parent=None, title="Wybierz plik", name_filter="Wszystkie pliki (*)"):
        super().__init__(parent, title)

        self._drag_position = QPoint()
        self._is_dragging = False
        self._drag_widgets = []

        self.setObjectName("styledFileDialog")
        self.setWindowTitle(get_window_title(title))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        self.setModal(True)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        self.setNameFilter(name_filter)
        icon_view_mode = getattr(QFileDialog.ViewMode, "Icon", None)
        if icon_view_mode is None:
            icon_view_mode = QFileDialog.ViewMode.List
        self.setViewMode(icon_view_mode)
        self.setMinimumSize(720, 520)
        self.resize(760, 560)

        self.setLabelText(QFileDialog.DialogLabel.LookIn, "Folder:")
        self.setLabelText(QFileDialog.DialogLabel.FileName, "Nazwa pliku:")
        self.setLabelText(QFileDialog.DialogLabel.FileType, "Typ pliku:")
        self.setLabelText(QFileDialog.DialogLabel.Accept, "Otwórz")
        self.setLabelText(QFileDialog.DialogLabel.Reject, "Anuluj")
        self._apply_dialog_style()

        self.header = QWidget(self)
        self.header.setObjectName("styledFileDialogHeader")
        self.header.setFixedHeight(52)

        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(22, 10, 12, 8)
        header_layout.setSpacing(12)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("styledFileDialogTitle")

        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("styledFileDialogCloseButton")
        self.close_button.setFixedSize(34, 34)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.reject)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_button)

        self.preview_label = QLabel("Podgląd obrazu")
        self.preview_label.setObjectName("styledFileDialogPreview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(130)

        dialog_layout = self.layout()
        if dialog_layout is not None:
            dialog_layout.setContentsMargins(14, 64, 14, 14)
            dialog_layout.setSpacing(8)
            dialog_layout.addWidget(self.preview_label, dialog_layout.rowCount(), 0, 1, dialog_layout.columnCount())

        self.currentChanged.connect(self.update_preview)
        self.filesSelected.connect(lambda files: files and self.update_preview(files[0]))

        self._register_drag_widget(self.header)
        self._register_drag_widget(self.title_label)
        self._style_internal_buttons()

    def _apply_dialog_style(self):
        self.setStyleSheet("""
            QFileDialog#styledFileDialog {
                background-color: #0f1020;
                border: 1px solid #7c3aed;
                border-radius: 18px;
                color: #f4edff;
                font-family: Figtree, Arial, sans-serif;
                font-size: 13px;
                font-weight: 700;
            }
            QFileDialog#styledFileDialog QWidget {
                background-color: #0f1020;
                color: #f4edff;
                font-family: Figtree, Arial, sans-serif;
                font-size: 13px;
                font-weight: 700;
            }
            QWidget#styledFileDialogHeader {
                background-color: #0f1020;
                border-top-left-radius: 18px;
                border-top-right-radius: 18px;
            }
            QLabel#styledFileDialogTitle {
                background-color: transparent;
                color: #ffffff;
                font-size: 15px;
                font-weight: 800;
            }
            QPushButton#styledFileDialogCloseButton {
                background-color: #7c3aed;
                border: none;
                border-radius: 12px;
                color: #ffffff;
                font-size: 18px;
                font-weight: 900;
                min-width: 34px;
                min-height: 34px;
                max-width: 34px;
                max-height: 34px;
                padding: 0;
            }
            QPushButton#styledFileDialogCloseButton:hover {
                background-color: #ef4444;
                color: #ffffff;
            }
            QPushButton#styledFileDialogCloseButton:pressed {
                background-color: #dc2626;
                color: #ffffff;
            }
            QLabel#styledFileDialogPreview {
                background-color: transparent;
                border: 1px dashed rgba(124, 58, 237, 0.65);
                border-radius: 14px;
                color: #d8ccff;
                font-weight: 800;
                padding: 12px;
            }
            QFrame, QSplitter, QStackedWidget {
                background-color: #111225;
                color: #f4edff;
            }
            QAbstractItemView, QListView, QTreeView {
                background-color: #111225;
                alternate-background-color: #15172d;
                border: 1px solid rgba(124, 58, 237, 0.55);
                border-radius: 10px;
                color: #ffffff;
                selection-background-color: #7c3aed;
                selection-color: #ffffff;
                padding: 6px;
                outline: none;
            }
            QAbstractItemView::item, QListView::item, QTreeView::item {
                background-color: transparent;
                color: #ffffff;
                min-height: 24px;
                padding: 4px 6px;
            }
            QAbstractItemView::item:selected, QListView::item:selected, QTreeView::item:selected {
                background-color: #7c3aed;
                color: #ffffff;
                border-radius: 6px;
            }
            QLabel {
                background-color: transparent;
                color: #d8ccff;
                font-weight: 800;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #8b5cf6;
                border-radius: 12px;
                color: #15151f;
                font-weight: 500;
                min-height: 34px;
                padding: 0 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #111225;
                border: 1px solid #7c3aed;
                color: #ffffff;
                selection-background-color: #7c3aed;
            }
            QPushButton, QDialogButtonBox QPushButton {
                background-color: #2f2550;
                border: 1px solid rgba(139, 92, 246, 0.75);
                border-radius: 12px;
                color: #ffffff;
                font-weight: 800;
                min-height: 36px;
                padding: 0 18px;
            }
            QPushButton:hover, QDialogButtonBox QPushButton:hover {
                background-color: #7c3aed;
                border-color: #a78bfa;
                color: #ffffff;
            }
            QPushButton:pressed, QDialogButtonBox QPushButton:pressed {
                background-color: #6d28d9;
                color: #ffffff;
            }
            QPushButton:disabled, QDialogButtonBox QPushButton:disabled {
                background-color: #2a2a3a;
                border-color: #4b5563;
                color: #cbd5e1;
            }
            QToolButton {
                background-color: #17182b;
                border: 1px solid rgba(124, 58, 237, 0.55);
                border-radius: 8px;
                color: #ffffff;
                icon-size: 18px 18px;
                min-width: 34px;
                min-height: 34px;
                padding: 2px;
            }
            QToolButton:hover {
                background-color: #2f2550;
                border-color: #a78bfa;
                color: #ffffff;
            }
            QToolButton:pressed {
                background-color: #6d28d9;
                color: #ffffff;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background-color: #18152b;
                border: none;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background-color: #7c3aed;
                border-radius: 6px;
                min-height: 28px;
                min-width: 28px;
            }
            QScrollBar::add-line, QScrollBar::sub-line,
            QScrollBar::add-page, QScrollBar::sub-page {
                background: none;
                border: none;
                width: 0;
                height: 0;
            }
        """)

    def _style_internal_buttons(self):
        for button in self.findChildren(QPushButton):
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            if button is not self.close_button:
                button.setMinimumHeight(36)
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #2f2550;
                        border: 1px solid rgba(139, 92, 246, 0.75);
                        border-radius: 12px;
                        color: #ffffff;
                        font-weight: 800;
                        min-height: 36px;
                        padding: 0 18px;
                    }
                    QPushButton:hover {
                        background-color: #7c3aed;
                        border-color: #a78bfa;
                        color: #ffffff;
                    }
                    QPushButton:pressed {
                        background-color: #6d28d9;
                        color: #ffffff;
                    }
                    QPushButton:disabled {
                        background-color: #2a2a3a;
                        border-color: #4b5563;
                        color: #cbd5e1;
                    }
                    """
                )

    def _apply_rounded_mask(self):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 18, 18)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

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
        if not self._is_dragging or event.buttons() != Qt.MouseButton.LeftButton:
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
        if event.position().y() <= self.header.height() and self._start_drag(event):
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._move_dragged_window(event):
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._is_dragging = False
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.header.setGeometry(0, 0, self.width(), 52)
        self._apply_rounded_mask()

    def showEvent(self, event):
        super().showEvent(event)
        self._style_internal_buttons()
        self._apply_rounded_mask()
        disable_windows_11_rounded_corners(self)

    def update_preview(self, file_path):
        if not file_path:
            self.preview_label.setText("Podgląd obrazu")
            self.preview_label.setPixmap(QPixmap())
            return

        path = Path(file_path)
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            self.preview_label.setText("Podgląd dostępny tylko dla obrazów")
            self.preview_label.setPixmap(QPixmap())
            return

        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            self.preview_label.setText("Nie udało się wczytać podglądu")
            self.preview_label.setPixmap(QPixmap())
            return

        scaled_pixmap = pixmap.scaled(
            180,
            120,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview_label.setText("")
        self.preview_label.setPixmap(scaled_pixmap)
