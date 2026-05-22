import requests

from tests.conftest import FakeResponse
import services.auth_service as auth_service


def test_login_returns_token_on_success(monkeypatch):
    def fake_post(url, json, verify, timeout):
        return FakeResponse(200, {"token": "jwt-token"})

    monkeypatch.setattr(auth_service.requests, "post", fake_post)

    assert auth_service.login("user@example.com", "Password1") == "jwt-token"


def test_login_returns_none_on_api_error(monkeypatch):
    def fake_post(url, json, verify, timeout):
        return FakeResponse(400, {"detail": "Błędne dane"})

    monkeypatch.setattr(auth_service.requests, "post", fake_post)

    assert auth_service.login("user@example.com", "wrong") is None


def test_login_returns_none_on_connection_error(monkeypatch):
    def fake_post(url, json, verify, timeout):
        raise requests.RequestException("connection error")

    monkeypatch.setattr(auth_service.requests, "post", fake_post)

    assert auth_service.login("user@example.com", "Password1") is None


def test_register_sends_expected_payload_and_handles_success(monkeypatch):
    captured = {}

    def fake_api_post(endpoint, data=None, auth_required=True):
        captured["endpoint"] = endpoint
        captured["data"] = data
        captured["auth_required"] = auth_required
        return FakeResponse(200, {})

    monkeypatch.setattr(auth_service, "api_post", fake_api_post)

    success, error = auth_service.register("user@example.com", "tester", "Password1")

    assert success is True
    assert error is None
    assert captured == {
        "endpoint": "/api/authentication/register",
        "data": {
            "email": "user@example.com",
            "username": "tester",
            "password": "Password1",
        },
        "auth_required": False,
    }


def test_register_returns_server_error_message(monkeypatch):
    def fake_api_post(endpoint, data=None, auth_required=True):
        return FakeResponse(400, {"detail": "Email jest już zajęty"})

    monkeypatch.setattr(auth_service, "api_post", fake_api_post)

    success, error = auth_service.register("user@example.com", "tester", "Password1")

    assert success is False
    assert error == "Email jest już zajęty"


def test_forgot_password_returns_true_for_status_200(monkeypatch):
    captured = {}

    def fake_api_post(endpoint, data=None, auth_required=True):
        captured["endpoint"] = endpoint
        captured["data"] = data
        captured["auth_required"] = auth_required
        return FakeResponse(200, {})

    monkeypatch.setattr(auth_service, "api_post", fake_api_post)

    assert auth_service.forgot_password("user@example.com") is True
    assert captured == {
        "endpoint": "/api/authentication/forgot-password",
        "data": {"email": "user@example.com"},
        "auth_required": False,
    }


def test_reset_password_sends_token_and_new_password(monkeypatch):
    captured = {}

    def fake_api_post(endpoint, data=None, auth_required=True):
        captured["endpoint"] = endpoint
        captured["data"] = data
        captured["auth_required"] = auth_required
        return FakeResponse(200, {})

    monkeypatch.setattr(auth_service, "api_post", fake_api_post)

    success, error = auth_service.reset_password("user@example.com", "token-value", "Password1")

    assert success is True
    assert error is None
    assert captured == {
        "endpoint": "/api/authentication/reset-password",
        "data": {
            "email": "user@example.com",
            "token": "token-value",
            "newPassword": "Password1",
        },
        "auth_required": False,
    }
