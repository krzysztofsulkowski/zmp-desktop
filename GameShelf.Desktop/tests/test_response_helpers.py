from tests.conftest import FakeResponse
from services.response_helpers import error_message, is_success, response_data, response_json


def test_response_json_returns_default_for_none():
    assert response_json(None, {"fallback": True}) == {"fallback": True}


def test_response_json_returns_default_when_json_is_invalid():
    response = FakeResponse(200, ValueError("bad json"))
    assert response_json(response, []) == []


def test_response_data_extracts_data_field_from_dict():
    response = FakeResponse(200, {"data": [1, 2, 3]})
    assert response_data(response, []) == [1, 2, 3]


def test_response_data_returns_plain_json_when_no_data_field():
    response = FakeResponse(200, [{"id": 1}])
    assert response_data(response, []) == [{"id": 1}]


def test_is_success_checks_expected_status_code():
    assert is_success(FakeResponse(201), 201) is True
    assert is_success(FakeResponse(400), 201) is False
    assert is_success(None) is False


def test_error_message_prefers_detail_title_message_then_default():
    assert error_message(FakeResponse(400, {"detail": "detail msg"}), "default") == "detail msg"
    assert error_message(FakeResponse(400, {"title": "title msg"}), "default") == "title msg"
    assert error_message(FakeResponse(400, {"message": "message msg"}), "default") == "message msg"
    assert error_message(FakeResponse(400, [], text="plain text"), "default") == "plain text"
    assert error_message(FakeResponse(400, {}), "default") == "default"
