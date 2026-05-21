import ctypes
import sys

try:
    from ctypes import wintypes
except ImportError:
    wintypes = None


def disable_windows_11_rounded_corners(widget):
    if sys.platform != "win32" or widget is None or wintypes is None:
        return

    try:
        hwnd = int(widget.winId())
        if hwnd == 0:
            return

        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        DWMWCP_DONOTROUND = 1
        preference = ctypes.c_int(DWMWCP_DONOTROUND)

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            ctypes.c_uint(DWMWA_WINDOW_CORNER_PREFERENCE),
            ctypes.byref(preference),
            ctypes.sizeof(preference)
        )
    except Exception:
        return
