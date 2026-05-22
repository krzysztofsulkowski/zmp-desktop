from pathlib import Path

from utils.security_validators import (
    MAX_AVATAR_SIZE_BYTES,
    validate_avatar_file,
    validate_bio,
    validate_email,
    validate_group_name,
    validate_message,
    validate_password,
    validate_username,
)


def test_validate_email_accepts_correct_address():
    assert validate_email("user@example.com") is True


def test_validate_email_rejects_invalid_address():
    assert validate_email("user-example.com") is False


def test_validate_password_requires_minimum_security_rules():
    assert validate_password("short")[0] is False
    assert validate_password("password1")[0] is False
    assert validate_password("PASSWORD1")[0] is False
    assert validate_password("Password1")[0] is True


def test_validate_username_accepts_safe_characters_only():
    assert validate_username("Aneta_123")[0] is True
    assert validate_username("ab")[0] is False
    assert validate_username("<script>")[0] is False


def test_validate_bio_message_and_group_name_limits():
    assert validate_bio("a" * 500)[0] is True
    assert validate_bio("a" * 501)[0] is False
    assert validate_message("Cześć")[0] is True
    assert validate_message("")[0] is False
    assert validate_message("a" * 1001)[0] is False
    assert validate_group_name("Grupa testowa")[0] is True
    assert validate_group_name("a" * 81)[0] is False


def test_validate_avatar_file_accepts_allowed_small_image(tmp_path):
    avatar_path = tmp_path / "avatar.png"
    avatar_path.write_bytes(b"test")

    assert validate_avatar_file(avatar_path)[0] is True


def test_validate_avatar_file_rejects_missing_wrong_extension_and_too_large_file(tmp_path):
    assert validate_avatar_file(tmp_path / "missing.png")[0] is False

    txt_path = tmp_path / "avatar.txt"
    txt_path.write_bytes(b"test")
    assert validate_avatar_file(txt_path)[0] is False

    large_path = tmp_path / "avatar.jpg"
    large_path.write_bytes(b"0" * (MAX_AVATAR_SIZE_BYTES + 1))
    assert validate_avatar_file(large_path)[0] is False
