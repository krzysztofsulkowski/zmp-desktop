import json

import services.app_settings_service as app_settings_service


def test_load_settings_returns_defaults_when_file_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(app_settings_service, "SETTINGS_FILE", tmp_path / "settings.json")

    assert app_settings_service.load_settings() == {"start_with_system": False}


def test_load_settings_merges_existing_file_with_defaults(monkeypatch, tmp_path):
    settings_file = tmp_path / "settings.json"
    settings_file.write_text(json.dumps({"start_with_system": True, "unknown": "value"}), encoding="utf-8")
    monkeypatch.setattr(app_settings_service, "SETTINGS_FILE", settings_file)

    assert app_settings_service.load_settings()["start_with_system"] is True


def test_load_settings_returns_defaults_for_invalid_json(monkeypatch, tmp_path):
    settings_file = tmp_path / "settings.json"
    settings_file.write_text("broken", encoding="utf-8")
    monkeypatch.setattr(app_settings_service, "SETTINGS_FILE", settings_file)

    assert app_settings_service.load_settings() == {"start_with_system": False}


def test_save_settings_writes_only_safe_boolean_value(monkeypatch, tmp_path):
    settings_file = tmp_path / "settings.json"
    monkeypatch.setattr(app_settings_service, "SETTINGS_FILE", settings_file)

    app_settings_service.save_settings({"start_with_system": 1, "other": "ignored"})

    assert json.loads(settings_file.read_text(encoding="utf-8")) == {"start_with_system": True}


def test_set_start_with_system_does_nothing_outside_windows(monkeypatch):
    monkeypatch.setattr(app_settings_service.sys, "platform", "linux")

    assert app_settings_service.set_start_with_system(True) is None
