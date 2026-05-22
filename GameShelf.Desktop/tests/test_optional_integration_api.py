import os

import pytest
import requests

API_URL = os.getenv("GAMESHELF_TEST_API_URL", "https://localhost:8081")
RUN_INTEGRATION = os.getenv("RUN_GAMESHELF_API_TESTS") == "1"

pytestmark = pytest.mark.integration


def _skip_when_disabled():
    if not RUN_INTEGRATION:
        pytest.skip("Optional API integration tests are disabled. Set RUN_GAMESHELF_API_TESTS=1 to run them.")


def test_api_swagger_is_reachable_when_integration_tests_are_enabled():
    _skip_when_disabled()

    response = requests.get(f"{API_URL}/swagger/index.html", verify=False, timeout=5)

    assert response.status_code == 200


def test_authentication_login_endpoint_exists_when_integration_tests_are_enabled():
    _skip_when_disabled()

    response = requests.post(
        f"{API_URL}/api/authentication/login",
        json={"email": "not-existing-user@example.com", "password": "Password1"},
        verify=False,
        timeout=5,
    )

    assert response.status_code in {400, 401}


def test_available_games_endpoint_requires_auth_or_returns_data_when_integration_tests_are_enabled():
    _skip_when_disabled()

    response = requests.post(
        f"{API_URL}/api/games/available-table",
        json={"draw": 1, "start": 0, "length": 5, "searchValue": "", "orderColumn": 0, "orderDir": "asc", "extraFilters": {}},
        verify=False,
        timeout=5,
    )

    assert response.status_code in {200, 401, 403}
