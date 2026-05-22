from datetime import datetime

from utils.datetime_formatter import format_datetime


def test_format_datetime_formats_iso_string_with_z_suffix():
    assert format_datetime("2026-05-22T11:30:00Z") == "22.05.2026 11:30"


def test_format_datetime_formats_datetime_object_in_compact_mode():
    value = datetime(2026, 5, 22, 11, 30)
    assert format_datetime(value, compact=True) == "22.05 11:30"


def test_format_datetime_returns_empty_for_empty_value():
    assert format_datetime(None) == ""
    assert format_datetime("") == ""


def test_format_datetime_returns_original_text_when_invalid():
    assert format_datetime("not a date") == "not a date"
