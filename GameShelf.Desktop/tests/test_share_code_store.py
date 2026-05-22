import services.share_code_store as share_code_store


def test_load_share_codes_returns_empty_dict_when_file_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(share_code_store, "STORE_PATH", tmp_path / "missing.json")

    assert share_code_store.load_share_codes() == {}


def test_load_share_codes_returns_empty_dict_for_invalid_json(monkeypatch, tmp_path):
    store = tmp_path / "share_codes.json"
    store.write_text("not-json", encoding="utf-8")
    monkeypatch.setattr(share_code_store, "STORE_PATH", store)

    assert share_code_store.load_share_codes() == {}


def test_save_share_code_persists_code_by_collection_id(monkeypatch, tmp_path):
    store = tmp_path / "share_codes.json"
    monkeypatch.setattr(share_code_store, "STORE_PATH", store)

    share_code_store.save_share_code(15, "ABC123")

    assert share_code_store.load_share_codes() == {"15": "ABC123"}
    assert share_code_store.get_share_code(15) == "ABC123"


def test_save_share_code_ignores_missing_collection_id_or_code(monkeypatch, tmp_path):
    store = tmp_path / "share_codes.json"
    monkeypatch.setattr(share_code_store, "STORE_PATH", store)

    share_code_store.save_share_code(None, "ABC")
    share_code_store.save_share_code(1, "")

    assert store.exists() is False
