import sys
import types

import requests

from tests.conftest import FakeResponse


class FakePixmap:
    def __init__(self, *args, **kwargs):
        self.loaded = False

    def isNull(self):
        return not self.loaded

    def loadFromData(self, data):
        self.loaded = bool(data)
        return self.loaded

    def scaled(self, *args, **kwargs):
        return self

    def copy(self, *args, **kwargs):
        return self

    def size(self):
        return self

    def fill(self, *args, **kwargs):
        return None

    def width(self):
        return 252

    def height(self):
        return 140


class FakePainter:
    Antialiasing = object()

    def __init__(self, *args, **kwargs):
        pass

    def setRenderHint(self, *args, **kwargs):
        return None

    def setClipPath(self, *args, **kwargs):
        return None

    def drawPixmap(self, *args, **kwargs):
        return None

    def end(self):
        return None


class FakePainterPath:
    def moveTo(self, *args, **kwargs):
        return None

    def lineTo(self, *args, **kwargs):
        return None

    def quadTo(self, *args, **kwargs):
        return None

    def closeSubpath(self):
        return None


class FakeQt:
    KeepAspectRatioByExpanding = object()
    SmoothTransformation = object()
    transparent = object()

    class AspectRatioMode:
        KeepAspectRatioByExpanding = object()

    class TransformationMode:
        SmoothTransformation = object()


qtcore_module = types.ModuleType("PySide6.QtCore")
qtcore_module.QRect = object
qtcore_module.Qt = FakeQt
qtgui_module = types.ModuleType("PySide6.QtGui")
qtgui_module.QPixmap = FakePixmap
qtgui_module.QPainter = FakePainter
qtgui_module.QPainterPath = FakePainterPath
pyside_module = types.ModuleType("PySide6")
sys.modules.setdefault("PySide6", pyside_module)
sys.modules.setdefault("PySide6.QtCore", qtcore_module)
sys.modules.setdefault("PySide6.QtGui", qtgui_module)

import services.avatar_service as avatar_service
from services.cover_image_service import CoverImageService


def test_normalized_avatar_url_returns_none_for_empty_value():
    assert avatar_service.normalized_avatar_url(None) is None
    assert avatar_service.normalized_avatar_url("") is None


def test_normalized_avatar_url_adds_api_url_for_relative_path():
    assert avatar_service.normalized_avatar_url("/avatars/a.png").endswith("/avatars/a.png")


def test_normalized_avatar_url_keeps_absolute_url():
    assert avatar_service.normalized_avatar_url("https://cdn.example.com/a.png") == "https://cdn.example.com/a.png"


def test_load_pixmap_from_url_returns_empty_pixmap_when_request_fails(monkeypatch):
    def fake_get(url, verify, timeout):
        raise requests.RequestException("network")

    monkeypatch.setattr(avatar_service.requests, "get", fake_get)

    assert avatar_service.load_pixmap_from_url("/avatar.png").isNull() is True


def test_load_pixmap_from_url_returns_empty_pixmap_for_non_200(monkeypatch):
    monkeypatch.setattr(avatar_service.requests, "get", lambda url, verify, timeout: FakeResponse(404, {}))

    assert avatar_service.load_pixmap_from_url("/avatar.png").isNull() is True


def test_cover_image_service_normalizes_relative_urls():
    service = CoverImageService()

    assert service.normalize_image_url("https://cdn.example.com/game.png") == "https://cdn.example.com/game.png"
    assert service.normalize_image_url("/covers/game.png").endswith("/covers/game.png")
    assert service.normalize_image_url("covers/game.png").endswith("/covers/game.png")


def test_cover_image_service_reuses_cached_cover(monkeypatch):
    calls = []
    response = FakeResponse(200, {})
    response.content = b"cover"

    def fake_get(url, verify, timeout):
        calls.append(url)
        return response

    monkeypatch.setattr("services.cover_image_service.requests.get", fake_get)
    service = CoverImageService()

    first = service.get_cached_cover("https://cdn.example.com/cover.png")
    second = service.get_cached_cover("https://cdn.example.com/cover.png")

    assert first is second
    assert len(calls) == 1
