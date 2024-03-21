from django.contrib import messages

from apps.seizures.views import SeizuresView


class SeizuresErrorView(SeizuresView):
    """Error handlers template view shows message with status code."""
    message = "Sorry, but unfortunately, there was an unknown error."
    status_code = 500

    def dispatch(self, request, *args, **kwargs):
        """Send error message in response."""
        messages.error(request=request, message=self.message)
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Set status code of the HTTP response."""
        response_kwargs["status"] = self.status_code
        return super().render_to_response(context, **response_kwargs)
