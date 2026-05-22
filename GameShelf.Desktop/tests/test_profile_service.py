import requests

from tests.conftest import FakeResponse
import services.profile_service as profile_service
import services.session as session


def test_build_profile_files_without_avatar_contains_username_and_bio():
    files = profile_service.build_profile_files("user", "bio", None)

    assert files == [("Username", (None, "user")), ("Bio", (None, "bio"))]
    assert profile_service.get_avatar_file(files) is None


def test_build_profile_files_with_avatar_opens_file_and_detects_mime_type(tmp_path):
    avatar = tmp_path / "avatar.png"
    avatar.write_bytes(b"png")

    files = profile_service.build_profile_files("user", "bio", str(avatar))
    avatar_file = profile_service.get_avatar_file(files)

    try:
        assert files[2][0] == "Avatar"
        assert files[2][1][0] == "avatar.png"
        assert files[2][1][2] == "image/png"
        assert avatar_file.read() == b"png"
    finally:
        avatar_file.close()


def test_update_profile_returns_error_when_token_is_missing():
    session.clear_token()
    assert profile_service.update_profile("user", "bio") == (False, "Brak tokena użytkownika.")


def test_update_profile_sends_put_request_with_auth_header_and_closes_avatar(monkeypatch, tmp_path):
    session.set_token("jwt-token")
    avatar = tmp_path / "avatar.png"
    avatar.write_bytes(b"png")
    captured = {}

    def fake_put(url, files, headers, verify, timeout):
        captured["url"] = url
        captured["files"] = files
        captured["headers"] = headers
        captured["avatar_file"] = profile_service.get_avatar_file(files)
        return FakeResponse(200, {})

    monkeypatch.setattr(profile_service.requests, "put", fake_put)

    assert profile_service.update_profile("user", "bio", str(avatar)) == (True, None)
    assert captured["url"].endswith("/api/authentication/update-profile")
    assert captured["headers"] == {"Authorization": "Bearer jwt-token"}
    assert captured["avatar_file"].closed is True


def test_update_profile_returns_api_error_message(monkeypatch):
    session.set_token("jwt-token")
    monkeypatch.setattr(
        profile_service.requests,
        "put",
        lambda url, files, headers, verify, timeout: FakeResponse(400, {"detail": "Zły avatar"}, text="raw"),
    )

    assert profile_service.update_profile("user", "bio") == (False, "Zły avatar")


def test_update_profile_returns_request_exception_message(monkeypatch):
    session.set_token("jwt-token")

    def fake_put(url, files, headers, verify, timeout):
        raise requests.RequestException("network error")

    monkeypatch.setattr(profile_service.requests, "put", fake_put)

    assert profile_service.update_profile("user", "bio") == (False, "network error")
