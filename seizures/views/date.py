from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from . import SeizuresBaseView


class SeizuresSearchDateView(SeizuresBaseView):
    """Search for seizures between a start and end time."""
    allow_empty = True
    http_method_names = ("get", "post")
    search_start = None
    search_end = None

    def setup(self, request, *args, **kwargs):
        """Set default search start and end datetime values."""

        if not self.search_end:
            self.search_end = timezone.localtime()

        if not self.search_start:
            self.search_start = self.search_end - settings.DEFAULT_SINCE

        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle date search form POST requests."""
        self.search_start = timezone.make_aware(
            parse_datetime(
                request.POST.get("search_start")
            )
        )
        self.search_end = timezone.make_aware(
            parse_datetime(
                request.POST.get("search_end")
            )
        )
        return self.get(request, args, kwargs)

    def get_queryset(self):
        """Filter seizures recorded between datetime values."""
        return super().get_queryset().filter(
            timestamp__gte=self.search_start,
            timestamp__lte=self.search_end
        )

    def get_context_data(self, *args, **kwargs):
        """Include start and end search times in context."""
        context = super().get_context_data(*args, **kwargs)
        context["search_start"] = self.search_start
        context["search_end"] = self.search_end
        return context

    def render_to_response(self, context, **response_kwargs):
        """Set initial/max value of the date search form fields."""
        dt_fmt = "%Y-%m-%dT%H:%M:%S"
        context["search_form"].set_values(
            start=self.search_start.strftime(dt_fmt),
            end=self.search_end.strftime(dt_fmt),
        )
        return super().render_to_response(context)

