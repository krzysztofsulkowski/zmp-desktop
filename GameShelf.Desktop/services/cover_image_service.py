import requests

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath

from config import API_URL, VERIFY_SSL


class CoverImageService:
    def __init__(self):
        self.cache = {}

    def set_cover_image(self, cover, game):
        image_url = getattr(game, "image_url", None)

        if not image_url:
            cover.setText(game.title)
            return

        normalized_url = self.normalize_image_url(image_url)
        pixmap = self.get_cached_cover(normalized_url)

        if pixmap is None or pixmap.isNull():
            cover.setText(game.title)
            return

        cropped = self.crop_pixmap(pixmap, 252, 140)
        cover.setPixmap(self.round_top_corners(cropped))

    def normalize_image_url(self, image_url):
        if image_url.startswith("http://") or image_url.startswith("https://"):
            return image_url

        if image_url.startswith("/"):
            return f"{API_URL}{image_url}"

        return f"{API_URL}/{image_url}"

    def get_cached_cover(self, image_url):
        if image_url in self.cache:
            return self.cache[image_url]

        pixmap = QPixmap()

        try:
            response = requests.get(image_url, verify=VERIFY_SSL, timeout=8)

            if response.status_code == 200:
                pixmap.loadFromData(response.content)
        except requests.RequestException:
            pass

        self.cache[image_url] = pixmap
        return pixmap

    def crop_pixmap(self, pixmap, width, height):
        scaled = pixmap.scaled(
            width,
            height,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        x = max(0, (scaled.width() - width) // 2)
        y = max(0, (scaled.height() - height) // 2)

        return scaled.copy(x, y, width, height)

    def round_top_corners(self, pixmap):
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        radius = 14.0
        width = pixmap.width()
        height = pixmap.height()

        path.moveTo(radius, 0)
        path.lineTo(width - radius, 0)
        path.quadTo(width, 0, width, radius)
        path.lineTo(width, height)
        path.lineTo(0, height)
        path.lineTo(0, radius)
        path.quadTo(0, 0, radius, 0)
        path.closeSubpath()

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rounded
