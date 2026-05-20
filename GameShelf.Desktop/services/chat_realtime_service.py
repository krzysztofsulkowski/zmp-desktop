from signalrcore.hub_connection_builder import HubConnectionBuilder

from config import CHAT_HUB_URL, VERIFY_SSL
from services.session import get_token


class ChatRealtimeService:
    def __init__(self, on_message_received):
        self.hub_connection = None
        self.on_message_received = on_message_received
        self.current_group_id = None
        self.is_connected = False

    def connect(self):
        token = get_token()

        if not token:
            return False

        try:
            self.hub_connection = HubConnectionBuilder() \
                .with_url(
                    CHAT_HUB_URL,
                    options={
                        "access_token_factory": lambda: token,
                        "verify_ssl": VERIFY_SSL
                    }
                ) \
                .build()

            self.hub_connection.on(
                "ReceiveMessage",
                self.handle_receive_message
            )

            self.hub_connection.start()
            self.is_connected = True

            return True
        except Exception:
            self.hub_connection = None
            self.is_connected = False
            return False

    def subscribe(self, group_id):
        if not self.hub_connection or not self.is_connected:
            return

        self.current_group_id = group_id

        try:
            self.hub_connection.send(
                "SubscribeToMessages",
                [group_id]
            )
        except Exception:
            self.is_connected = False

    def unsubscribe(self, group_id):
        if not self.hub_connection or not self.is_connected:
            return

        try:
            self.hub_connection.send(
                "UnsubscribeFromMessages",
                [group_id]
            )
        except Exception:
            self.is_connected = False

    def send_message(self, group_id, content):
        if not self.hub_connection or not self.is_connected:
            return False

        try:
            self.hub_connection.send(
                "SendMessageToGroup",
                [group_id, content]
            )
            return True
        except Exception:
            self.is_connected = False
            return False

    def handle_receive_message(self, args):
        if not args:
            return

        message = args[0]
        self.on_message_received(message)

    def stop(self):
        if not self.hub_connection:
            return

        try:
            self.hub_connection.stop()
        except Exception:
            pass
        finally:
            self.hub_connection = None
            self.is_connected = False