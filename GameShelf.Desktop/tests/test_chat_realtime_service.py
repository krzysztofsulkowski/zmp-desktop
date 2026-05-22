import sys
import types

import services.session as session


class PlaceholderHubBuilder:
    pass

signalrcore_module = types.ModuleType("signalrcore")
hub_builder_module = types.ModuleType("signalrcore.hub_connection_builder")
hub_builder_module.HubConnectionBuilder = PlaceholderHubBuilder
sys.modules.setdefault("signalrcore", signalrcore_module)
sys.modules.setdefault("signalrcore.hub_connection_builder", hub_builder_module)

import services.chat_realtime_service as realtime_module
from services.chat_realtime_service import ChatRealtimeService


class FakeHubConnection:
    def __init__(self, fail_send=False):
        self.handlers = {}
        self.sent = []
        self.started = False
        self.stopped = False
        self.fail_send = fail_send

    def on(self, event_name, callback):
        self.handlers[event_name] = callback

    def start(self):
        self.started = True

    def send(self, method, args):
        if self.fail_send:
            raise RuntimeError("send failed")
        self.sent.append((method, args))

    def stop(self):
        self.stopped = True


class FakeHubBuilder:
    def __init__(self, connection):
        self.connection = connection
        self.url = None
        self.options = None

    def with_url(self, url, options):
        self.url = url
        self.options = options
        return self

    def build(self):
        return self.connection


def test_connect_returns_false_without_token():
    session.clear_token()
    service = ChatRealtimeService(lambda message: None)

    assert service.connect() is False
    assert service.is_connected is False


def test_connect_builds_hub_connection_and_registers_receive_handler(monkeypatch):
    session.set_token("jwt-token")
    connection = FakeHubConnection()
    builder = FakeHubBuilder(connection)
    monkeypatch.setattr(realtime_module, "HubConnectionBuilder", lambda: builder)

    service = ChatRealtimeService(lambda message: None)

    assert service.connect() is True
    assert service.is_connected is True
    assert connection.started is True
    assert "ReceiveMessage" in connection.handlers
    assert builder.options["access_token_factory"]() == "jwt-token"


def test_subscribe_unsubscribe_and_send_message_send_expected_hub_methods(monkeypatch):
    service = ChatRealtimeService(lambda message: None)
    connection = FakeHubConnection()
    service.hub_connection = connection
    service.is_connected = True

    service.subscribe(5)
    service.unsubscribe(5)
    success = service.send_message(5, "Hej")

    assert success is True
    assert connection.sent == [
        ("SubscribeToMessages", [5]),
        ("UnsubscribeFromMessages", [5]),
        ("SendMessageToGroup", [5, "Hej"]),
    ]


def test_send_message_returns_false_and_marks_disconnected_on_exception():
    service = ChatRealtimeService(lambda message: None)
    service.hub_connection = FakeHubConnection(fail_send=True)
    service.is_connected = True

    assert service.send_message(5, "Hej") is False
    assert service.is_connected is False


def test_handle_receive_message_ignores_empty_args_and_forwards_first_message():
    received = []
    service = ChatRealtimeService(received.append)

    service.handle_receive_message([])
    service.handle_receive_message([{"content": "Hej"}, {"content": "Drugie"}])

    assert received == [{"content": "Hej"}]


def test_stop_clears_connection_and_marks_disconnected():
    service = ChatRealtimeService(lambda message: None)
    connection = FakeHubConnection()
    service.hub_connection = connection
    service.is_connected = True

    service.stop()

    assert connection.stopped is True
    assert service.hub_connection is None
    assert service.is_connected is False
