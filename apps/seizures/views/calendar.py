from .base import SeizuresBaseView


class SeizuresCalendarView(SeizuresBaseView):
    """fullcalendar view."""
    days = 30
    template_name = "calendar.html"
