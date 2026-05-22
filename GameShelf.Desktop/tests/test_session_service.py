import services.session as session


def test_set_get_and_clear_token():
    session.set_token("jwt-token")

    assert session.get_token() == "jwt-token"

    session.clear_token()

    assert session.get_token() is None


def test_setting_empty_token_is_returned_as_empty_value():
    session.set_token("")

    assert session.get_token() == ""

    session.clear_token()
