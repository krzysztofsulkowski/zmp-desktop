from services.notifications_service import NotificationsService


def test_load_read_notifications_returns_empty_set_when_file_missing(tmp_path):
    service = NotificationsService(tmp_path / "missing.json")
    assert service.load_read_notifications() == set()


def test_load_read_notifications_returns_empty_set_for_invalid_json(tmp_path):
    path = tmp_path / "notifications.json"
    path.write_text("not-json", encoding="utf-8")

    service = NotificationsService(path)
    assert service.load_read_notifications() == set()


def test_save_and_load_read_notifications(tmp_path):
    path = tmp_path / "notifications.json"
    service = NotificationsService(path)

    service.save_read_notifications({"b", "a"})

    assert service.load_read_notifications() == {"a", "b"}
    assert path.read_text(encoding="utf-8").strip().startswith("[")


def test_get_notifications_builds_friend_request_notifications(monkeypatch, tmp_path):
    import services.notifications_service as notifications_module

    monkeypatch.setattr(
        notifications_module,
        "get_pending_requests",
        lambda: [
            {"userName": "Aneta", "userId": 10},
            {"username": "Krzysiek", "id": 20},
            {},
        ],
    )

    service = NotificationsService(tmp_path / "notifications.json")
    notifications = service.get_notifications()

    assert notifications[0]["id"] == "friend_request:10"
    assert notifications[0]["title"] == "Zaproszenie do znajomych"
    assert "Aneta" in notifications[0]["content"]
    assert notifications[1]["id"] == "friend_request:20"
    assert notifications[2]["id"] == "friend_request:Nieznany użytkownik"
