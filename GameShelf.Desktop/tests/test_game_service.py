import requests

from tests.conftest import FakeResponse
import services.game_service as game_service


def test_get_available_games_returns_data_from_table_response(monkeypatch):
    monkeypatch.setattr(
        game_service,
        "api_post",
        lambda endpoint, data: FakeResponse(200, {"data": [{"id": 1, "title": "Game"}]}),
    )

    assert game_service.get_available_games() == [{"id": 1, "title": "Game"}]


def test_get_available_games_returns_empty_list_for_invalid_json(monkeypatch):
    monkeypatch.setattr(game_service, "api_post", lambda endpoint, data: FakeResponse(200, ValueError("bad")))
    assert game_service.get_available_games() == []


def test_add_remove_move_game_return_boolean_from_status(monkeypatch):
    monkeypatch.setattr(game_service, "api_post", lambda endpoint, data=None: FakeResponse(200, {}))
    monkeypatch.setattr(game_service, "api_delete", lambda endpoint: FakeResponse(500, {}))

    assert game_service.add_game_to_collection(1, 2) is True
    assert game_service.move_game(1, 2, 3) is True
    assert game_service.remove_game_from_collection(1) is False


def test_rate_game_returns_success_and_error_variants(monkeypatch):
    monkeypatch.setattr(game_service, "api_post", lambda endpoint, data: FakeResponse(200, {}))
    assert game_service.rate_game(1, 5) == (True, None)

    monkeypatch.setattr(game_service, "api_post", lambda endpoint, data: None)
    assert game_service.rate_game(1, 5) == (False, "Brak połączenia z API.")

    monkeypatch.setattr(game_service, "api_post", lambda endpoint, data: FakeResponse(400, {"detail": "Błąd"}))
    assert game_service.rate_game(1, 5) == (False, {"detail": "Błąd"})


def test_get_game_genres_and_platforms_use_fallbacks(monkeypatch):
    monkeypatch.setattr(game_service, "api_get", lambda endpoint: FakeResponse(200, ["RPG"]))
    assert game_service.get_game_genres() == ["RPG"]

    monkeypatch.setattr(game_service, "api_get", lambda endpoint: FakeResponse(500, {}))
    assert game_service.get_game_platforms() == []


def test_propose_game_sends_data_and_image_file(monkeypatch, tmp_path):
    image_path = tmp_path / "cover.png"
    image_path.write_bytes(b"img")
    captured = {}

    def fake_post(url, data, files, headers, verify, timeout):
        captured["url"] = url
        captured["data"] = data
        captured["files"] = files
        return FakeResponse(200, {})

    monkeypatch.setattr(game_service.requests, "post", fake_post)
    monkeypatch.setattr(game_service, "get_headers", lambda: {"Authorization": "Bearer token"})

    assert game_service.propose_game("Title", "Desc", 1, 2, str(image_path)) is True
    assert captured["data"] == {"title": "Title", "description": "Desc", "genreId": "1", "platformId": "2"}
    assert "image" in captured["files"]


def test_propose_game_returns_false_on_request_exception(monkeypatch):
    def fake_send(data, image_path):
        raise requests.RequestException("network")

    monkeypatch.setattr(game_service, "_send_game_proposal", fake_send)
    assert game_service.propose_game("Title", "Desc", 1, 2) is False
