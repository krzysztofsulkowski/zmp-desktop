from tests.conftest import FakeResponse
import services.statistics_service as statistics_service
import services.user_service as user_service


def test_get_my_library_statistics_returns_json_for_success(monkeypatch):
    monkeypatch.setattr(statistics_service, "api_get", lambda endpoint: FakeResponse(200, {"totalGames": 3}))

    assert statistics_service.get_my_library_statistics() == {"totalGames": 3}


def test_get_my_library_statistics_returns_none_for_error(monkeypatch):
    monkeypatch.setattr(statistics_service, "api_get", lambda endpoint: FakeResponse(500, {}))

    assert statistics_service.get_my_library_statistics() is None


def test_get_global_statistics_returns_json_for_success(monkeypatch):
    monkeypatch.setattr(statistics_service, "api_get", lambda endpoint: FakeResponse(200, {"users": 10}))

    assert statistics_service.get_global_statistics() == {"users": 10}


def test_get_global_statistics_returns_none_when_api_is_unavailable(monkeypatch):
    monkeypatch.setattr(statistics_service, "api_get", lambda endpoint: None)

    assert statistics_service.get_global_statistics() is None


def test_get_current_user_returns_profile_for_success(monkeypatch):
    monkeypatch.setattr(user_service, "get_me", lambda: FakeResponse(200, {"email": "user@example.com"}))

    assert user_service.get_current_user() == {"email": "user@example.com"}


def test_get_current_user_returns_empty_dict_for_error(monkeypatch):
    monkeypatch.setattr(user_service, "get_me", lambda: FakeResponse(401, {}))

    assert user_service.get_current_user() == {}
