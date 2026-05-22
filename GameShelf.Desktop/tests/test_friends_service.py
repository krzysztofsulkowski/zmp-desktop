from tests.conftest import FakeResponse
import services.friends_service as friends_service


def test_get_my_friends_returns_list_on_success(monkeypatch):
    monkeypatch.setattr(friends_service, "api_get", lambda endpoint: FakeResponse(200, [{"id": 1}]))
    assert friends_service.get_my_friends() == [{"id": 1}]


def test_get_my_friends_returns_empty_list_on_error(monkeypatch):
    monkeypatch.setattr(friends_service, "api_get", lambda endpoint: FakeResponse(500, {}))
    assert friends_service.get_my_friends() == []


def test_search_users_sends_expected_table_payload(monkeypatch):
    captured = {}

    def fake_post(endpoint, data):
        captured["endpoint"] = endpoint
        captured["data"] = data
        return FakeResponse(200, {"data": [{"username": "ana"}]})

    monkeypatch.setattr(friends_service, "api_post", fake_post)

    assert friends_service.search_users("ana") == [{"username": "ana"}]
    assert captured["endpoint"] == "/api/friends/search"
    assert captured["data"]["searchValue"] == "ana"
    assert captured["data"]["length"] == 20


def test_add_friend_by_username_encodes_username_and_returns_success(monkeypatch):
    captured = {}

    def fake_post(endpoint):
        captured["endpoint"] = endpoint
        return FakeResponse(200, {})

    monkeypatch.setattr(friends_service, "api_post", fake_post)

    success, message = friends_service.add_friend_by_username("ana test")

    assert success is True
    assert message == "Zaproszenie zostało wysłane."
    assert captured["endpoint"].endswith("ana%20test")


def test_add_friend_by_username_returns_api_error_message(monkeypatch):
    monkeypatch.setattr(
        friends_service,
        "api_post",
        lambda endpoint: FakeResponse(400, {"detail": "Już wysłano zaproszenie."}),
    )

    success, message = friends_service.add_friend_by_username("ana")

    assert success is False
    assert message == "Już wysłano zaproszenie."


def test_accept_friend_request_and_reject_friend_handle_connection_error(monkeypatch):
    monkeypatch.setattr(friends_service, "api_post", lambda endpoint: None)
    monkeypatch.setattr(friends_service, "api_delete", lambda endpoint: None)

    assert friends_service.accept_friend_request(1) == (False, "Brak połączenia z API.")
    assert friends_service.reject_or_remove_friend(1) == (False, "Brak połączenia z API.")
