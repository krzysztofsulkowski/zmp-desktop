from services.session import get_token
from services.auth_service import get_user_profile

from views.landing_view import LandingView
from views.login_view import LoginView
from views.register_view import RegisterView
from views.main_view import MainView
from views.forgot_password_view import ForgotPasswordView
from views.reset_password_view import ResetPasswordView



class AppController:
    def __init__(self):
        self.landing_view = None
        self.login_view = None
        self.register_view = None
        self.main_view = None
        self.forgot_password_view = None
        self.reset_password_view = None

    def close_all_views(self):
        for view in [
            self.landing_view,
            self.login_view,
            self.register_view,
            self.main_view,
            self.forgot_password_view,
            self.reset_password_view
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
        if not get_token():
            self.show_login()
            return

        user_profile = get_user_profile()

        if not user_profile:
            self.show_login()
            return

        self.close_all_views()
        self.main_view = MainView(self)
        self.main_view.show()

    def show_forgot_password(self):
        self.close_all_views()
        self.forgot_password_view = ForgotPasswordView(self)
        self.forgot_password_view.show()

    def show_reset_password(self):
        self.close_all_views()
        self.reset_password_view = ResetPasswordView(
            self.show_login
        )
        self.reset_password_view.show()