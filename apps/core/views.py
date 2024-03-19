from django.contrib import messages
from django.views.generic.base import TemplateView


class SeizuresErrorView(TemplateView):
    """Error handlers template view shows message with status code."""
    message = "Sorry, but unfortunately, there was an unknown error."
    status_code = 500
    template_name = "seizures.html"

    def dispatch(self, request, *args, **kwargs):
        messages.error(request=request,message=self.message)
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(
            context,
            **response_kwargs,
            status=self.status_code
        )
