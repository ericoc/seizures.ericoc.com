from apps.seizures.views import SeizuresBaseView


class SeizuresErrorView(SeizuresBaseView):
    """Error handler template view returns message with status code."""
    days = 0
    message = "Sorry, but unfortunately, there was an unknown error."
    status_code = 500
    template_name = "error.html"

    def get_context_data(self, **kwargs):
        # Include error message in context.
        context = super().get_context_data(**kwargs)
        context["message"] = self.message
        return context

    def render_to_response(self, context, **response_kwargs):
        # Set status code of the HTTP response.
        response_kwargs["status"] = self.status_code
        return super().render_to_response(context, **response_kwargs)
