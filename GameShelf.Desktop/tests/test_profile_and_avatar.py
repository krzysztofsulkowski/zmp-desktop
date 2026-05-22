from pathlib import Path

import requests

from tests.conftest import FakeResponse
import services.profile_service as profile_service


def test_build_profile_files_without_avatar_contains_username_and_bio_only():
    files = profile_service.build_profile_files("tester", "Moje bio", None)

    assert files == [
        ("Username", (None, "tester")),
        ("Bio", (None, "Moje bio")),
    ]
    assert profile_service.get_avatar_file(files) is None


def test_build_profile_files_with_avatar_adds_file_part(tmp_path):
    avatar_path = tmp_path / "avatar.png"
    avatar_path.write_bytes(b"avatar")

    files = profile_service.build_profile_files("tester", "Bio", str(avatar_path))
    avatar_file = profile_service.get_avatar_file(files)

    assert files[0] == ("Username", (None, "tester"))
    assert files[1] == ("Bio", (None, "Bio"))
    assert files[2][0] == "Avatar"
    assert files[2][1][0] == "avatar.png"
    assert files[2][1][2] == "image/png"
    assert avatar_file.read() == b"avatar"
    avatar_file.close()


def test_update_profile_returns_error_when_token_is_missing(monkeypatch):
    monkeypatch.setattr(profile_service, "get_token", lambda: None)

    success, error = profile_service.update_profile("tester", "Bio")

    assert success is False
    assert error == "Brak tokena użytkownika."


def test_update_profile_sends_put_request_with_authorization(monkeypatch, tmp_path):
    captured = {}
    avatar_path = tmp_path / "avatar.jpg"
    avatar_path.write_bytes(b"avatar")

    monkeypatch.setattr(profile_service, "get_token", lambda: "jwt-token")

    def fake_put(url, files, headers, verify, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["fields"] = [(name, value[0]) for name, value in files]
        captured["avatar_name"] = files[2][1][0]
        return FakeResponse(200, {})

    monkeypatch.setattr(profile_service.requests, "put", fake_put)

    success, error = profile_service.update_profile("tester", "Bio", str(avatar_path))

    assert success is True
    assert error is None
    assert captured["url"].endswith("/api/authentication/update-profile")
    assert captured["headers"] == {"Authorization": "Bearer jwt-token"}
    assert captured["fields"] == [("Username", None), ("Bio", None), ("Avatar", "avatar.jpg")]
    assert captured["avatar_name"] == "avatar.jpg"


def test_update_profile_returns_request_error(monkeypatch):
    monkeypatch.setattr(profile_service, "get_token", lambda: "jwt-token")

    def fake_put(url, files, headers, verify, timeout):
        raise requests.RequestException("network error")

    monkeypatch.setattr(profile_service.requests, "put", fake_put)

    success, error = profile_service.update_profile("tester", "Bio")

    assert success is False
    assert "network error" in error
