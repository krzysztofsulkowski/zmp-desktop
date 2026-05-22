import os

import pytest
import requests
from dotenv import load_dotenv
from PySide6.QtCore import Qt

load_dotenv()

pytestmark = pytest.mark.e2e


class E2EConfig:
    def __init__(self):
        from config import API_URL, VERIFY_SSL

        self.api_url = os.getenv("GAMESHELF_E2E_API_URL", os.getenv("GAMESHELF_TEST_API_URL", API_URL)).rstrip("/")
        self.email = os.getenv("GAMESHELF_E2E_EMAIL", "").strip()
        self.password = os.getenv("GAMESHELF_E2E_PASSWORD", "")
        self.username = os.getenv("GAMESHELF_E2E_USERNAME", "").strip()
        self.verify_ssl = os.getenv("GAMESHELF_E2E_VERIFY_SSL", str(VERIFY_SSL)).lower() == "true"
        self.timeout = int(os.getenv("GAMESHELF_E2E_TIMEOUT", "10"))


def _skip_when_e2e_disabled(config):
    if os.getenv("RUN_GAMESHELF_E2E_TESTS") != "1":
        pytest.skip("E2E tests are disabled. Set RUN_GAMESHELF_E2E_TESTS=1 to run them.")

    if not config.email or not config.password:
        pytest.skip("Set GAMESHELF_E2E_EMAIL and GAMESHELF_E2E_PASSWORD in .env to run E2E tests.")


@pytest.fixture(scope="session")
def e2e_config():
    config = E2EConfig()
    _skip_when_e2e_disabled(config)
    return config


@pytest.fixture(scope="session")
def e2e_token(e2e_config):
    response = requests.post(
        f"{e2e_config.api_url}/api/authentication/login",
        json={"email": e2e_config.email, "password": e2e_config.password},
        verify=e2e_config.verify_ssl,
        timeout=e2e_config.timeout,
    )

    assert response.status_code == 200

    token = response.json().get("token")

    assert isinstance(token, str)
    assert token.strip()

    return token


@pytest.fixture()
def auth_headers(e2e_token):
    return {"Authorization": f"Bearer {e2e_token}"}


@pytest.fixture()
def desktop_session_token(e2e_token):
    from services.session import clear_token, set_token

    clear_token()
    set_token(e2e_token)
    yield e2e_token
    clear_token()


def test_e2e_api_is_reachable(e2e_config):
    response = requests.get(
        f"{e2e_config.api_url}/swagger/index.html",
        verify=e2e_config.verify_ssl,
        timeout=e2e_config.timeout,
    )

    assert response.status_code == 200


def test_e2e_user_can_login_and_receive_token(e2e_token):
    assert e2e_token.count(".") >= 1


def test_e2e_logged_user_profile_can_be_loaded(e2e_config, auth_headers):
    response = requests.get(
        f"{e2e_config.api_url}/api/authentication/me",
        headers=auth_headers,
        verify=e2e_config.verify_ssl,
        timeout=e2e_config.timeout,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data.get("email") or data.get("userName") or data.get("username")


def test_e2e_desktop_session_reads_current_user_through_service(desktop_session_token):
    from services.user_service import get_current_user

    user = get_current_user()

    assert isinstance(user, dict)
    assert user


def test_e2e_desktop_auth_service_reads_profile(desktop_session_token):
    from services.auth_service import get_user_profile

    profile = get_user_profile()

    assert isinstance(profile, dict)
    assert profile


def test_e2e_collections_lookup_returns_list_for_logged_user(desktop_session_token):
    from services.collection_service import get_collections_lookup

    collections = get_collections_lookup()

    assert isinstance(collections, list)

    for collection in collections:
        assert isinstance(collection, dict)
        assert "id" in collection
        assert "name" in collection


def test_e2e_grouped_collection_games_endpoint_returns_expected_shape(e2e_config, auth_headers):
    response = requests.post(
        f"{e2e_config.api_url}/api/collections/grouped-with-games",
        json={"draw": 1, "start": 0, "length": 10, "searchValue": "", "orderColumn": 0, "orderDir": "asc", "extraFilters": {}},
        headers=auth_headers,
        verify=e2e_config.verify_ssl,
        timeout=e2e_config.timeout,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)


def test_e2e_available_games_are_loaded_by_desktop_service(desktop_session_token):
    from services.game_service import get_available_games

    games = get_available_games()

    assert isinstance(games, list)

    for game in games[:5]:
        assert isinstance(game, dict)
        assert "id" in game
        assert "title" in game


def test_e2e_game_genres_and_platforms_are_loaded(desktop_session_token):
    from services.game_service import get_game_genres, get_game_platforms

    genres = get_game_genres()
    platforms = get_game_platforms()

    assert isinstance(genres, list)
    assert isinstance(platforms, list)


def test_e2e_statistics_endpoints_are_available_for_logged_user(desktop_session_token):
    from services.statistics_service import get_global_statistics, get_my_library_statistics

    my_statistics = get_my_library_statistics()
    global_statistics = get_global_statistics()

    assert my_statistics is None or isinstance(my_statistics, dict)
    assert global_statistics is None or isinstance(global_statistics, dict)


def test_e2e_friends_services_return_safe_lists(desktop_session_token):
    from services.friends_service import get_my_friends, get_pending_requests, search_users

    friends = get_my_friends()
    pending_requests = get_pending_requests()
    users = search_users("")

    assert isinstance(friends, list)
    assert isinstance(pending_requests, list)
    assert isinstance(users, list)


def test_e2e_notifications_can_be_built_from_api_requests(desktop_session_token, tmp_path):
    from services.notifications_service import NotificationsService

    service = NotificationsService(tmp_path / "notifications_read.json")
    notifications = service.get_notifications()

    assert isinstance(notifications, list)

    for notification in notifications:
        assert notification.get("id")
        assert notification.get("title")
        assert notification.get("content")


def test_e2e_chat_list_and_first_chat_messages_can_be_loaded(desktop_session_token):
    from services.chat_service import get_chat_messages, get_my_chats

    chats = get_my_chats()

    assert isinstance(chats, list)

    if not chats:
        return

    first_chat = chats[0]
    group_id = first_chat.get("id") or first_chat.get("groupId")

    if not group_id:
        return

    messages = get_chat_messages(group_id)

    assert isinstance(messages, list)


def test_e2e_invalid_reset_token_is_rejected_without_changing_password(e2e_config):
    response = requests.post(
        f"{e2e_config.api_url}/api/authentication/reset-password",
        json={"email": e2e_config.email, "token": "invalid-e2e-token", "newPassword": "Password123!"},
        verify=e2e_config.verify_ssl,
        timeout=e2e_config.timeout,
    )

    assert response.status_code in {400, 401, 404}


def test_e2e_desktop_login_view_logs_user_in(qtbot, e2e_config):
    from services.session import clear_token, get_token
    from views.login_view import LoginView

    class Controller:
        def __init__(self):
            self.main_opened = False

        def show_main(self):
            self.main_opened = True

        def show_forgot_password(self):
            pass

        def show_register(self):
            pass

    clear_token()
    controller = Controller()
    view = LoginView(controller)
    qtbot.addWidget(view)

    view.email_input.setText(e2e_config.email)
    view.password_input.setText(e2e_config.password)
    qtbot.mouseClick(view.login_button, Qt.MouseButton.LeftButton)

    assert controller.main_opened is True
    assert get_token()
    assert "Zalogowano" in view.status_label.text()

    clear_token()
