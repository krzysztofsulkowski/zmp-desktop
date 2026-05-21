import http.server
import queue
import socket
import socketserver
import threading
import urllib.parse
import webbrowser

import requests

from config import API_URL, VERIFY_SSL
from services.api_client import api_get, api_post


class _GoogleCallbackHandler(http.server.BaseHTTPRequestHandler):
    result_queue = None

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)
        token = params.get("token", [None])[0]
        error = params.get("error", [None])[0]

        if token:
            self.result_queue.put((token, None))
            message = "Logowanie zakończone. Możesz wrócić do aplikacji GameShelf."
            status = 200
        else:
            self.result_queue.put((None, error or "Nie udało się zalogować przez Google."))
            message = "Nie udało się zakończyć logowania. Wróć do aplikacji GameShelf i spróbuj ponownie."
            status = 400

        body = f"""
        <!doctype html>
        <html lang="pl">
        <head><meta charset="utf-8"><title>GameShelf</title></head>
        <body style="font-family: Arial, sans-serif; background:#0f0f1a; color:#fff; display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0;">
            <div style="max-width:520px; padding:32px; border:1px solid #8B5CF6; border-radius:24px; background:#151125; text-align:center;">
                <h1 style="margin-top:0;">GameShelf</h1>
                <p>{message}</p>
            </div>
        </body>
        </html>
        """.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def _find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def login(email, password):
    url = f"{API_URL}/api/authentication/login"

    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(
            url,
            json=data,
            verify=VERIFY_SSL,
            timeout=10
        )
    except requests.RequestException:
        return None

    if response.status_code == 200:
        return response.json().get("token")

    return None


def login_with_google(timeout_seconds=180):
    result_queue = queue.Queue(maxsize=1)
    port = _find_free_port()
    callback_url = f"http://127.0.0.1:{port}/google-callback"
    encoded_callback_url = urllib.parse.quote(callback_url, safe="")
    auth_url = f"{API_URL}/api/authentication/external-login?provider=Google&returnUrl={encoded_callback_url}"

    _GoogleCallbackHandler.result_queue = result_queue

    try:
        with socketserver.TCPServer(("127.0.0.1", port), _GoogleCallbackHandler) as server:
            server.timeout = timeout_seconds
            server_thread = threading.Thread(target=server.handle_request, daemon=True)
            server_thread.start()

            opened = webbrowser.open(auth_url, new=2)
            if not opened:
                return None, "Nie udało się otworzyć przeglądarki do logowania Google."

            try:
                token, error = result_queue.get(timeout=timeout_seconds)
            except queue.Empty:
                return None, "Przekroczono czas oczekiwania na logowanie przez Google."
            finally:
                server.server_close()

            if token:
                return token, None

            return None, error or "Logowanie przez Google nie powiodło się."
    except OSError:
        return None, "Nie udało się uruchomić lokalnego odbioru logowania Google."


def get_user_profile():
    response = api_get("/api/authentication/me")

    if response is None or response.status_code != 200:
        return {}

    return response.json()


def logout():
    api_post("/api/authentication/logout")


def register(email, username, password):
    data = {
        "email": email,
        "username": username,
        "password": password
    }

    response = api_post(
        "/api/authentication/register",
        data,
        auth_required=False
    )

    if response is None:
        return False, "Nie udało się połączyć z API."

    if response.status_code == 200:
        return True, None

    try:
        error_data = response.json()
        return False, error_data.get("detail", "Rejestracja nie powiodła się.")
    except Exception:
        return False, "Rejestracja nie powiodła się."


def forgot_password(email):
    data = {
        "email": email
    }

    response = api_post(
        "/api/authentication/forgot-password",
        data,
        auth_required=False
    )

    if response is None:
        return False

    return response.status_code == 200


def reset_password(email, token, new_password):
    data = {
        "email": email,
        "token": token,
        "newPassword": new_password
    }

    response = api_post(
        "/api/authentication/reset-password",
        data,
        auth_required=False
    )

    if response is None:
        return False, "Brak połączenia z API."

    if response.status_code == 200:
        return True, None

    try:
        return False, response.json()
    except Exception:
        return False, response.text
