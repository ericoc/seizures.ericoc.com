from django.contrib.auth.views import LoginView, LogoutView


class SeizuresLoginView(LoginView):
    """Log in view."""
    template_name = "login.html"


class SeizuresLogoutView(LogoutView):
    """Log out view."""
    template_name = "login.html"
