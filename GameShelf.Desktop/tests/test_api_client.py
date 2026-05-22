import requests

from tests.conftest import FakeResponse
import services.api_client as api_client
import services.session as session


def test_api_get_adds_authorization_header_when_token_exists(monkeypatch):
    captured = {}
    session.set_token("jwt-token")

    def fake_request(method, url, json, headers, verify, timeout):
        captured["method"] = method
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers
        captured["verify"] = verify
        captured["timeout"] = timeout
        return FakeResponse(200, {"ok": True})

    monkeypatch.setattr(api_client.requests, "request", fake_request)

    response = api_client.api_get("/api/authentication/me")

    assert response.status_code == 200
    assert captured["method"] == "GET"
    assert captured["url"].endswith("/api/authentication/me")
    assert captured["headers"] == {"Authorization": "Bearer jwt-token"}


def test_api_post_without_auth_does_not_add_authorization_header(monkeypatch):
    captured = {}
    session.set_token("jwt-token")

    def fake_request(method, url, json, headers, verify, timeout):
        captured["method"] = method
        captured["json"] = json
        captured["headers"] = headers
        return FakeResponse(200, {})

    monkeypatch.setattr(api_client.requests, "request", fake_request)

    api_client.api_post("/api/authentication/register", {"email": "user@example.com"}, auth_required=False)

    assert captured["method"] == "POST"
    assert captured["json"] == {"email": "user@example.com"}
    assert captured["headers"] == {}


def test_api_request_clears_token_on_unauthorized(monkeypatch):
    session.set_token("jwt-token")

    def fake_request(method, url, json, headers, verify, timeout):
        return FakeResponse(401, {})

    monkeypatch.setattr(api_client.requests, "request", fake_request)

    response = api_client.api_get("/api/protected")

    assert response.status_code == 401
    assert session.get_token() is None


def test_api_request_returns_none_on_connection_error(monkeypatch):
    def fake_request(method, url, json, headers, verify, timeout):
        raise requests.RequestException("connection error")

    monkeypatch.setattr(api_client.requests, "request", fake_request)

    assert api_client.api_get("/api/protected") is None


def test_build_url_joins_api_url_and_endpoint():
    assert api_client.build_url("/api/test").endswith("/api/test")


def test_get_headers_returns_empty_dict_when_no_token():
    session.clear_token()
    assert api_client.get_headers() == {}


def test_get_headers_returns_empty_dict_when_auth_not_required():
    session.set_token("jwt-token")
    assert api_client.get_headers(auth_required=False) == {}


def test_api_put_and_delete_use_expected_methods(monkeypatch):
    methods = []

    def fake_request(method, url, json, headers, verify, timeout):
        methods.append((method, json))
        return FakeResponse(200, {})

    monkeypatch.setattr(api_client.requests, "request", fake_request)

    api_client.api_put("/api/item", {"id": 1})
    api_client.api_delete("/api/item/1")

    assert methods == [("PUT", {"id": 1}), ("DELETE", None)]


def test_get_me_calls_authentication_me_endpoint(monkeypatch):
    captured = {}

    def fake_request(method, url, json, headers, verify, timeout):
        captured["url"] = url
        return FakeResponse(200, {"email": "user@example.com"})

    monkeypatch.setattr(api_client.requests, "request", fake_request)

    response = api_client.get_me()

    assert response.status_code == 200
    assert captured["url"].endswith("/api/authentication/me")
