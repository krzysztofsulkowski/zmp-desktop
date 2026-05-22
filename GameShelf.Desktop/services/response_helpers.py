def response_json(response, default=None):
    if response is None:
        return default

    try:
        return response.json()
    except Exception:
        return default


def response_data(response, default=None):
    data = response_json(response, default)

    if isinstance(data, dict) and "data" in data:
        return data.get("data") or default

    return data


def is_success(response, status_code=200):
    return response is not None and response.status_code == status_code


def error_message(response, default_message):
    data = response_json(response, {})

    if isinstance(data, dict):
        return data.get("detail") or data.get("title") or data.get("message") or default_message

    if response is not None and getattr(response, "text", None):
        return response.text

    return default_message
