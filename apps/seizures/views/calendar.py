from .base import SeizuresBaseView


class SeizuresCalendarView(SeizuresBaseView):
    """fullcalendar view."""
    days = 365
    template_name = "calendar.html"
