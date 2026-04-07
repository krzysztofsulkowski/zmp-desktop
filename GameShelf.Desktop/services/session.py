_token = None


def set_token(token):
    global _token
    _token = token


def get_token():
    return _token


def clear_token():
    global _token
    _token = None