from django.views.generic import  RedirectView


class SeizuresMainView(RedirectView):
    """Main view redirects to map."""
    pattern_name = "map"
