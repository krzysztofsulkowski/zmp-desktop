from math import atan2, degrees

from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtCore import QPoint, Qt, QRectF, QMargins
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QToolTip, QVBoxLayout, QWidget


STAT_COLORS = [
    "#5C4E7E",
    "#7D6EA1",
    "#9C8BC5",
    "#BFB2DE",
    "#DED6F0",
    "#FFFFFF",
]


class DonutChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []
        self.slices = []
        self.hover_index = None
        self.colors = [QColor(color) for color in STAT_COLORS[:5]]
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
            inside = end <= angle <= current if current >= end else angle >= end or angle <= current

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


class GlobalStatsCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("globalStatsCard")
        self.setFixedSize(320, 320)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 18, 20, 18)
        self.layout.setSpacing(12)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("globalStatsCardTitle")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)


class PodiumBar(QWidget):
    def __init__(self, name, value, color, height):
        super().__init__()
        self.setObjectName("podiumBarWrapper")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("podiumValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bar = QFrame()
        self.bar.setObjectName("podiumBar")
        self.bar.setFixedSize(54, height)
        self.bar.setStyleSheet(f"QFrame#podiumBar {{ background-color: {color}; border-radius: 10px 10px 4px 4px; }}")
        self.name_label = QLabel(name)
        self.name_label.setObjectName("podiumName")
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setFixedWidth(86)
        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.bar, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.name_label)


def create_global_pie_chart_view():
    chart = QChart()
    chart.legend().hide()
    chart.setBackgroundVisible(False)
    chart.setPlotAreaBackgroundVisible(False)
    chart.setMargins(QMargins(0, 0, 0, 0))
    chart_view = QChartView(chart)
    chart_view.setObjectName("globalStatsChartView")
    chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
    chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    chart_view.setMinimumHeight(210)
    return chart, chart_view


def build_global_pie_chart(chart, items, parent):
    chart.removeAllSeries()
    series = QPieSeries()
    series.setHoleSize(0.48)
    series.setPieSize(0.84)

    for index, item in enumerate(items[:6]):
        label = item.get("label", "Brak")
        value = item.get("value", 0)
        slice_item = series.append(label, value)
        color = QColor(STAT_COLORS[index % len(STAT_COLORS)])
        slice_item.setBrush(color)
        slice_item.setBorderColor(color)
        slice_item.setLabelVisible(False)
        slice_item.hovered.connect(lambda state, l=label, v=value: show_slice_tooltip(state, l, v, parent))

    chart.addSeries(series)


def show_slice_tooltip(state, label, value, parent):
    if state:
        QToolTip.showText(parent.cursor().pos(), f"{label}: {value}", parent)
    else:
        QToolTip.hideText()


def create_podium_layout():
    podium_layout = QHBoxLayout()
    podium_layout.setContentsMargins(0, 8, 0, 0)
    podium_layout.setSpacing(10)
    podium_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
    return podium_layout
