from django.views.generic import  RedirectView


class SeizuresMainView(RedirectView):
    """Main view redirects to calendar."""
    pattern_name = "calendar"
