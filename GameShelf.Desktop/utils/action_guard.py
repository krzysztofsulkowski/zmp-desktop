from contextlib import contextmanager


@contextmanager
def disabled_while_running(button):
    button.setEnabled(False)
    try:
        yield
    finally:
        button.setEnabled(True)
