import queue as queue_module

from tests.conftest import FakeResponse
import services.auth_service as auth_service


def test_find_free_port_returns_integer_port():
    port = auth_service._find_free_port()

    assert isinstance(port, int)
    assert port > 0


def test_get_user_profile_returns_empty_dict_when_api_fails(monkeypatch):
    monkeypatch.setattr(auth_service, "api_get", lambda endpoint: FakeResponse(500, {}))

    assert auth_service.get_user_profile() == {}


def test_get_user_profile_returns_json_when_api_succeeds(monkeypatch):
    monkeypatch.setattr(auth_service, "api_get", lambda endpoint: FakeResponse(200, {"userName": "tester"}))

    assert auth_service.get_user_profile() == {"userName": "tester"}


def test_login_with_google_returns_error_when_browser_does_not_open(monkeypatch):
    monkeypatch.setattr(auth_service, "_find_free_port", lambda: 54321)
    monkeypatch.setattr(auth_service.webbrowser, "open", lambda url, new=2: False)

    token, error = auth_service.login_with_google(timeout_seconds=1)

    assert token is None
    assert error == "Nie udało się otworzyć przeglądarki do logowania Google."


def test_login_with_google_returns_timeout_message(monkeypatch):
    class FakeServer:
        def __init__(self, address, handler):
            self.timeout = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def handle_request(self):
            return None

        def server_close(self):
            return None

    monkeypatch.setattr(auth_service.socketserver, "TCPServer", FakeServer)
    monkeypatch.setattr(auth_service.webbrowser, "open", lambda url, new=2: True)
    OriginalQueue = queue_module.Queue
    monkeypatch.setattr(auth_service.queue, "Queue", lambda maxsize=1: OriginalQueue(maxsize=1))

    token, error = auth_service.login_with_google(timeout_seconds=0.01)

    assert token is None
    assert error == "Przekroczono czas oczekiwania na logowanie przez Google."
