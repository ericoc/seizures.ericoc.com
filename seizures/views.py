from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.views.generic import ListView
from django.views.generic.dates import (
    BaseDateListView, DayArchiveView, MonthArchiveView, YearArchiveView
)
from rest_framework import permissions, viewsets

from seizures.models import Seizure
from seizures.serializers import (
    UserSerializer, GroupSerializer, SeizureSerializer
)
from seizures.util import seize_context


class APIGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint for groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class APIUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class APISeizureViewSet(viewsets.ModelViewSet):
    """
    API endpoint for seizures.
    """
    queryset = Seizure.objects.all()
    serializer_class = SeizureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = "__all__"


class SeizureAllView(PermissionRequiredMixin, ListView):
    """
    Seizures list all view.
    """
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    model = Seizure
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html.djt"

    def get_context_data(self, *args, **kwargs):
        """Include context information about seizures and their locations."""
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureArchiveView(PermissionRequiredMixin, BaseDateListView):
    """
    List seizures during a specific time period using generic archive views.
    """
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    make_object_list = True
    model = Seizure
    month_format = "%m"
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html.djt"

    def get_context_data(self, *args, **kwargs):
        """Include context information about seizures and their locations."""
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureDayView(SeizureArchiveView, DayArchiveView):
    """
    List seizures on a specific day.
    """
    pass


class SeizureMonthView(SeizureArchiveView, MonthArchiveView):
    """
    List seizures during a specific month.
    """
    pass


class SeizureYearView(SeizureArchiveView, YearArchiveView):
    """
    List seizures during a specific year.
    """
    pass


class SeizureSinceView(PermissionRequiredMixin, ListView):
    """
    Seizure list view for the most recent X amount of time.
    """
    allow_empty = True
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    model = Seizure
    since_delta = settings.DEFAULT_SINCE
    since_when = None
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html.djt"

    def setup(self, request, *args, **kwargs):
        """Adjust look-back timedelta, if requested."""
        if kwargs.get("minutes"):
            self.since_delta = timedelta(minutes=kwargs.get("minutes"))

        if kwargs.get("hours"):
            self.since_delta = timedelta(hours=kwargs.get("hours"))

        if kwargs.get("days"):
            self.since_delta = timedelta(days=kwargs.get("days"))

        if kwargs.get("weeks"):
            self.since_delta = timedelta(weeks=kwargs.get("weeks"))

        if kwargs.get("months"):
            self.since_delta = timedelta(days=kwargs.get("months")*30)

        if kwargs.get("years"):
            self.since_delta = timedelta(days=kwargs.get("years")*365)

        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Calculate the look-back datetime using the requested timedelta."""
        self.since_when = timezone.now() - self.since_delta
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """Filter seizures recorded since the look-back timedelta."""
        return super().get_queryset().filter(timestamp__gte=self.since_when)

    def get_context_data(self, *args, **kwargs):
        """Include context information about seizures and their locations."""
        return seize_context(super().get_context_data(*args, **kwargs))
