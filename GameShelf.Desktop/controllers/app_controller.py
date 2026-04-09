from views.landing_view import LandingView
from views.login_view import LoginView
from views.register_view import RegisterView
from views.main_view import MainView
from views.forgot_password_view import ForgotPasswordView



class AppController:
    def __init__(self):
        self.landing_view = None
        self.login_view = None
        self.register_view = None
        self.main_view = None
        self.forgot_password_view = None

    def close_all_views(self):
        for view in [
            self.landing_view,
            self.login_view,
            self.register_view,
            self.main_view,
            self.forgot_password_view
        ]:
            if view:
                view.close()

    def show_landing(self):
        self.close_all_views()
        self.landing_view = LandingView(self)
        self.landing_view.show()

    def show_login(self):
        self.close_all_views()
        self.login_view = LoginView(self)
        self.login_view.show()

    def show_register(self):
        self.close_all_views()
        self.register_view = RegisterView(self)
        self.register_view.show()

    def show_main(self):
        self.close_all_views()
        self.main_view = MainView(self)
        self.main_view.show()

    def show_forgot_password(self):
        self.close_all_views()
        self.forgot_password_view = ForgotPasswordView(self)
        self.forgot_password_view.show()