from views.login_view import LoginView
from views.main_view import MainView


class AppController:
    def __init__(self):
        self.login_view = None
        self.main_view = None

    def show_login(self):
        if self.main_view:
            self.main_view.close()

        self.login_view = LoginView(self)
        self.login_view.show()

    def show_main(self):
        if self.login_view:
            self.login_view.close()

        self.main_view = MainView(self)
        self.main_view.show()