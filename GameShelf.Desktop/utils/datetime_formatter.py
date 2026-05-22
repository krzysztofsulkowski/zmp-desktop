from datetime import datetime


def format_datetime(value, compact=False):
    if not value:
        return ""

    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).replace("Z", "+00:00")

        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return str(value)

    if compact:
        return parsed.strftime("%d.%m %H:%M")

    return parsed.strftime("%d.%m.%Y %H:%M")
