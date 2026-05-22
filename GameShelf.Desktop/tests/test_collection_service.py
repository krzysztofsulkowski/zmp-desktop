from tests.conftest import FakeResponse
import services.collection_service as collection_service


def test_get_available_game_images_maps_ids_to_image_urls(monkeypatch):
    monkeypatch.setattr(
        collection_service,
        "api_post",
        lambda endpoint, data: FakeResponse(200, {"data": [
            {"id": 1, "imageUrl": "/covers/a.png"},
            {"id": 2, "imageUrl": ""},
            {"id": None, "imageUrl": "/covers/b.png"},
        ]}),
    )

    assert collection_service.get_available_game_images() == {1: "/covers/a.png"}


def test_get_game_rating_returns_rounded_rating_or_none(monkeypatch):
    monkeypatch.setattr(collection_service, "api_get", lambda endpoint: FakeResponse(200, "4.26"))
    assert collection_service.get_game_rating(1) == 4.3

    monkeypatch.setattr(collection_service, "api_get", lambda endpoint: FakeResponse(200, "0"))
    assert collection_service.get_game_rating(1) is None

    monkeypatch.setattr(collection_service, "api_get", lambda endpoint: FakeResponse(200, ValueError("bad")))
    assert collection_service.get_game_rating(1) is None


def test_get_my_collection_builds_game_models_with_fallback_image_and_rating(monkeypatch):
    monkeypatch.setattr(collection_service, "get_available_game_images", lambda: {10: "/covers/fallback.png"})
    monkeypatch.setattr(collection_service, "get_game_rating", lambda game_id: 4.5)

    def fake_post(endpoint, data):
        return FakeResponse(200, {"data": [{
            "collectionId": 5,
            "games": [{
                "gameId": 10,
                "title": "Game",
                "genreName": "RPG",
                "platformName": "PC",
                "imageUrl": None,
            }],
        }]})

    monkeypatch.setattr(collection_service, "api_post", fake_post)

    games = collection_service.get_my_collection()

    assert len(games) == 1
    assert games[0].game_id == 10
    assert games[0].title == "Game"
    assert games[0].image_url == "/covers/fallback.png"
    assert games[0].collection_id == 5
    assert games[0].rating == 4.5


def test_get_sorted_collections_sorts_case_insensitive(monkeypatch):
    monkeypatch.setattr(
        collection_service,
        "get_collections_lookup",
        lambda: [{"id": 2, "name": "zeta"}, {"id": 1, "name": "Alpha"}],
    )

    assert [collection["id"] for collection in collection_service.get_sorted_collections()] == [1, 2]


def test_get_current_collection_returns_matching_collection_or_none(monkeypatch):
    monkeypatch.setattr(collection_service, "get_collections_lookup", lambda: [{"id": 1}, {"id": 2}])

    assert collection_service.get_current_collection(2) == {"id": 2}
    assert collection_service.get_current_collection(3) is None


def test_create_collection_saves_share_code_and_returns_true(monkeypatch):
    captured = {}

    def fake_post(endpoint, data):
        captured["endpoint"] = endpoint
        captured["data"] = data
        return FakeResponse(200, {"id": 7, "shareCode": "ABC"})

    def fake_save_share_code(collection_id, share_code):
        captured["share"] = (collection_id, share_code)

    monkeypatch.setattr(collection_service, "api_post", fake_post)
    monkeypatch.setattr(collection_service, "save_share_code", fake_save_share_code)

    assert collection_service.create_collection("Nowa", True) is True
    assert captured["endpoint"] == "/api/collections/create"
    assert captured["data"] == {"id": 0, "name": "Nowa", "isPublic": True}
    assert captured["share"] == (7, "ABC")


def test_update_and_delete_collection_return_boolean_from_status(monkeypatch):
    monkeypatch.setattr(collection_service, "api_put", lambda endpoint, data: FakeResponse(200, {}))
    monkeypatch.setattr(collection_service, "api_delete", lambda endpoint: FakeResponse(404, {}))

    assert collection_service.update_collection(1, "Name", False) is True
    assert collection_service.delete_collection(1) is False
