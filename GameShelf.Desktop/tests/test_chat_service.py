from tests.conftest import FakeResponse
import services.chat_service as chat_service


def test_get_my_chats_returns_list_on_success(monkeypatch):
    expected_chats = [{"id": 1, "groupName": "Test"}]

    def fake_api_get(endpoint):
        assert endpoint == "/api/chat/my-chats"
        return FakeResponse(200, expected_chats)

    monkeypatch.setattr(chat_service, "api_get", fake_api_get)

    assert chat_service.get_my_chats() == expected_chats


def test_get_chat_messages_returns_empty_list_on_error(monkeypatch):
    def fake_api_get(endpoint):
        assert endpoint == "/api/chat/12/messages"
        return FakeResponse(500, {"detail": "error"})

    monkeypatch.setattr(chat_service, "api_get", fake_api_get)

    assert chat_service.get_chat_messages(12) == []


def test_create_chat_sends_group_name_and_user_ids(monkeypatch):
    captured = {}
    expected_response = {"id": 7, "groupName": "Ekipa"}

    def fake_api_post(endpoint, data=None):
        captured["endpoint"] = endpoint
        captured["data"] = data
        return FakeResponse(200, expected_response)

    monkeypatch.setattr(chat_service, "api_post", fake_api_post)

    success, result = chat_service.create_chat("Ekipa", [1, 2])

    assert success is True
    assert result == expected_response
    assert captured == {
        "endpoint": "/api/chat/create",
        "data": {"groupName": "Ekipa", "userIds": [1, 2]},
    }


def test_create_chat_returns_message_when_api_is_unavailable(monkeypatch):
    def fake_api_post(endpoint, data=None):
        return None

    monkeypatch.setattr(chat_service, "api_post", fake_api_post)

    success, message = chat_service.create_chat("Ekipa", [1])

    assert success is False
    assert message == "Brak połączenia z API."
