from math import atan2, degrees

from PySide6.QtCore import QPoint, Qt, QRectF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QSizePolicy,
    QScrollArea,
)

from services.statistics_service import get_my_library_statistics


class DonutChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []
        self.slices = []
        self.hover_index = None
        self.colors = [
            QColor("#5C4E7E"),
            QColor("#7D6EA1"),
            QColor("#9C8BC5"),
            QColor("#BFB2DE"),
            QColor("#FFFFFF"),
        ]
        self.tooltip = QLabel(self)
        self.tooltip.setObjectName("chartTooltip")
        self.tooltip.hide()
        self.setMouseTracking(True)
        self.setMinimumSize(180, 180)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_data(self, items):
        self.items = [
            {
                "label": str(item.get("label") or "Brak"),
                "value": int(item.get("value") or 0),
            }
            for item in items
            if int(item.get("value") or 0) > 0
        ]
        self.hover_index = None
        self.tooltip.hide()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        total = sum(item["value"] for item in self.items)
        if total <= 0:
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Brak danych")
            return

        side = min(self.width(), self.height()) - 18
        if side < 80:
            return

        left = (self.width() - side) / 2
        top = (self.height() - side) / 2
        rect = QRectF(left, top, side, side)

        pen_width = max(30, int(side * 0.22))
        pen_rect = rect.adjusted(pen_width / 2, pen_width / 2, -pen_width / 2, -pen_width / 2)

        start_angle = 90 * 16
        self.slices = []

        for index, item in enumerate(self.items):
            span_angle = int(round((item["value"] / total) * 360 * 16))
            color = self.colors[index % len(self.colors)]

            pen = QPen(color, pen_width)
            pen.setCapStyle(Qt.PenCapStyle.FlatCap)
            painter.setPen(pen)
            painter.drawArc(pen_rect, start_angle, -span_angle)

            self.slices.append((start_angle, -span_angle))
            start_angle -= span_angle

    def mouseMoveEvent(self, event):
        index = self.slice_at(event.position().toPoint())

        if index is None:
            self.hover_index = None
            self.tooltip.hide()
            self.update()
            return

        self.hover_index = index
        item = self.items[index]
        self.tooltip.setText(f'{item["label"]}: {item["value"]}')
        self.tooltip.adjustSize()

        x = event.position().toPoint().x() + 14
        y = event.position().toPoint().y() + 14

        if x + self.tooltip.width() > self.width():
            x = self.width() - self.tooltip.width() - 8
        if y + self.tooltip.height() > self.height():
            y = self.height() - self.tooltip.height() - 8

        self.tooltip.move(max(8, x), max(8, y))
        self.tooltip.show()
        self.update()

    def leaveEvent(self, event):
        self.hover_index = None
        self.tooltip.hide()
        self.update()

    def slice_at(self, point):
        total = sum(item["value"] for item in self.items)
        if total <= 0:
            return None

        side = min(self.width(), self.height()) - 18
        if side < 80:
            return None

        center = QPoint(self.width() // 2, self.height() // 2)
        dx = point.x() - center.x()
        dy = point.y() - center.y()
        distance = (dx * dx + dy * dy) ** 0.5

        outer_radius = side / 2
        inner_radius = outer_radius * 0.52

        if distance < inner_radius or distance > outer_radius:
            return None

        angle = (degrees(atan2(-dy, dx)) + 360) % 360
        current = 90

        for index, item in enumerate(self.items):
            span = (item["value"] / total) * 360
            end = (current - span) % 360

            if current >= end:
                inside = end <= angle <= current
            else:
                inside = angle >= end or angle <= current

            if inside:
                return index

            current = end

        return None


class StatsCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("statsCard")
        self.setFixedSize(320, 320)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(10)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("statsCardTitle")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.title_label)


class StatsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("statsView")
        self.cards = []
        self.current_columns = 0

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(36, 28, 36, 28)
        self.main_layout.setSpacing(26)

        self.title_label = QLabel("Twoje statystyki")
        self.title_label.setObjectName("statsPageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("statsScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("statsScrollWidget")
        self.grid = QGridLayout(self.scroll_widget)
        self.grid.setContentsMargins(0, 0, 0, 24)
        self.grid.setHorizontalSpacing(14)
        self.grid.setVerticalSpacing(26)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.total_card, self.total_value_label = self.create_number_card(
            "posiadasz następującą liczbę gier w swojej bibliotece:"
        )
        self.recent_card, self.recent_value_label = self.create_number_card(
            "liczba ostatnio dodanych gier w Twojej bibliotece:"
        )
        self.genre_card, self.genre_chart = self.create_chart_card(
            "liczba gier z podziałem na kategorie:"
        )
        self.platform_card, self.platform_chart = self.create_chart_card(
            "liczba gier z podziałem na platformy:"
        )
        self.collection_card, self.collection_chart = self.create_chart_card(
            "liczba gier z podziałem na kolekcje:"
        )

        self.cards = [
            self.total_card,
            self.recent_card,
            self.genre_card,
            self.platform_card,
            self.collection_card,
        ]

        self.rebuild_grid(3)
        self.load_statistics()

    def create_number_card(self, title):
        card = StatsCard(title)

        value_label = QLabel("0")
        value_label.setObjectName("statsNumber")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card.layout.addStretch(1)
        card.layout.addWidget(value_label)
        card.layout.addStretch(2)

        return card, value_label

    def create_chart_card(self, title):
        card = StatsCard(title)

        chart = DonutChartWidget()
        card.layout.addWidget(chart, 1)

        return card, chart

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grid_columns()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_grid_columns()
        self.load_statistics()

    def update_grid_columns(self):
        card_width = 320
        gap = 14

        viewport_width = self.scroll_area.viewport().width()
        window_width = self.window().width() - 210 if self.window() else 0
        available_width = max(viewport_width, window_width)

        columns = max(1, min(3, (available_width + gap) // (card_width + gap)))

        if available_width >= 1000:
            columns = 3
        elif available_width >= 660:
            columns = 2
        else:
            columns = 1

        self.rebuild_grid(columns)

    def rebuild_grid(self, columns):
        if self.current_columns == columns:
            return

        self.current_columns = columns

        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for index, card in enumerate(self.cards):
            row = index // columns
            column = index % columns
            self.grid.addWidget(card, row, column, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def load_statistics(self):
        stats = get_my_library_statistics()

        if not stats:
            self.total_value_label.setText("-")
            self.recent_value_label.setText("-")
            return

        self.total_value_label.setText(str(stats.get("totalGames", 0)))
        self.recent_value_label.setText(str(stats.get("addedRecentlyCount", 0)))

        self.genre_chart.set_data(stats.get("gamesByGenre", []))
        self.platform_chart.set_data(stats.get("gamesByPlatform", []))
        self.collection_chart.set_data(stats.get("gamesByCollection", []))
