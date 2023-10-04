from datetime import timedelta
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.serializers import serialize
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView
from django.views.generic.dates import (
    BaseDateListView, DayArchiveView, MonthArchiveView, YearArchiveView
)
from rest_framework import permissions, viewsets

from seizures.forms import SeizureSearchDateForm
from seizures.models import Seizure
from seizures.serializers import UserSerializer, SeizureSerializer


def seize_context(context=None):
    """JSON-serialize seizure data, and device icons, in response contexts."""
    seizures = context.get("seizures")
    context["search_form"] = SeizureSearchDateForm()
    if seizures:
        context["seizures"] = serialize(format="json", queryset=seizures)
        if settings.DEVICE_ICONS:
            context["device_icons"] = settings.DEVICE_ICONS
    return context


class APIUserViewSet(viewsets.ModelViewSet):
    """API endpoint for users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class APISeizureViewSet(viewsets.ModelViewSet):
    """API endpoint for seizures."""
    queryset = Seizure.objects.all()
    serializer_class = SeizureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = "__all__"


class SeizureLoginView(LoginView):
    """Log in view."""
    template_name = "login.html.djt"


class SeizureLogoutView(LogoutView):
    """Log out view."""
    template_name = "login.html.djt"


class SeizureBaseArchiveView(PermissionRequiredMixin, BaseDateListView):
    """List seizures during time period, using generic archive views."""
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    make_object_list = True
    model = Seizure
    month_format = "%m"
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html.djt"

    def get_context_data(self, *args, **kwargs):
        """Include seizures data in context information."""
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureDayView(SeizureBaseArchiveView, DayArchiveView):
    """List seizures on a specific day."""
    pass


class SeizureMonthView(SeizureBaseArchiveView, MonthArchiveView):
    """List seizures during a specific month."""
    pass


class SeizureYearView(SeizureBaseArchiveView, YearArchiveView):
    """List seizures during a specific year."""
    pass


class SeizureAllView(PermissionRequiredMixin, ListView):
    """Seizures list all view."""
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    model = Seizure
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html.djt"

    def get_context_data(self, *args, **kwargs):
        """Include seizures data in context information."""
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureSinceView(SeizureAllView):
    """Seizure list view for the most recent X amount of time."""
    allow_empty = True
    http_method_names = ("get", "post")
    since_delta = settings.DEFAULT_SINCE
    since_when = None

    def setup(self, request, *args, **kwargs):
        """Adjust look-back timedelta, if requested."""

        if kwargs.get("since_when"):
            self.since_when = kwargs.get("since_when")

        if self.since_when is None:

            if kwargs.get("minutes"):
                self.since_delta = timedelta(minutes=kwargs.get("minutes"))

            if kwargs.get("hours"):
                self.since_delta = timedelta(hours=kwargs.get("hours"))

            if kwargs.get("days"):
                self.since_delta = timedelta(days=kwargs.get("days"))

            if kwargs.get("weeks"):
                self.since_delta = timedelta(weeks=kwargs.get("weeks"))

            if kwargs.get("months"):
                self.since_delta = relativedelta(months=kwargs.get("months"))

            if kwargs.get("years"):
                self.since_delta = relativedelta(years=kwargs.get("years"))

        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        searched_date = request.POST.get("search_date")
        if searched_date:
            try:
                self.since_when = parse_datetime(searched_date)
            except ValueError:
                messages.warning(
                    request=request,
                    message="Sorry, but the search date could not be parsed."
                )
        return self.get(request, args, kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Calculate the look-back datetime using the requested timedelta."""
        if not self.since_when:
            if self.since_delta:
                self.since_when = timezone.localtime() - self.since_delta
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """Filter seizures recorded since the look-back datetime."""
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(timestamp__gte=self.since_when)

    def get_context_data(self, *args, **kwargs):
        """Include seizures data in context information, with look-back time."""
        context = super().get_context_data(*args, **kwargs)
        context["since_when"] = self.since_when

        # Set the initial value of the date search form.
        context["search_form"].fields["search_date"].initial = (
            self.since_when.strftime("%Y-%m-%dT%H:%M:%S")
        )

        return context
