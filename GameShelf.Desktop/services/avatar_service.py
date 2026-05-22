import requests

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPainter, QPainterPath, QPixmap

from config import API_URL, VERIFY_SSL

REQUEST_TIMEOUT = 10


def normalized_avatar_url(avatar_url):
    if not avatar_url:
        return None

    if avatar_url.startswith("/"):
        return f"{API_URL}{avatar_url}"

    return avatar_url


def load_pixmap_from_url(url):
    normalized_url = normalized_avatar_url(url)

    if not normalized_url:
        return QPixmap()

    try:
        response = requests.get(normalized_url, verify=VERIFY_SSL, timeout=REQUEST_TIMEOUT)
    except requests.RequestException:
        return QPixmap()

    if response.status_code != 200:
        return QPixmap()

    pixmap = QPixmap()
    pixmap.loadFromData(response.content)
    return pixmap


def create_round_pixmap(pixmap, size):
    if pixmap.isNull():
        return QPixmap()

    scaled = pixmap.scaled(
        size,
        size,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation,
    )

    x = max(0, (scaled.width() - size) // 2)
    y = max(0, (scaled.height() - size) // 2)
    cropped = scaled.copy(QRect(x, y, size, size))

    rounded = QPixmap(size, size)
    rounded.fill(Qt.GlobalColor.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, cropped)
    painter.end()

    return rounded


def load_round_avatar(avatar_url, size):
    return create_round_pixmap(load_pixmap_from_url(avatar_url), size)
