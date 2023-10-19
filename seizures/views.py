from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.serializers import serialize
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from rest_framework import permissions, viewsets

from seizures.forms import SeizuresSearchDateForm
from seizures.models import Seizure
from seizures.serializers import UserSerializer, SeizureSerializer


class APIUsersViewSet(viewsets.ModelViewSet):
    """API endpoint for users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class APISeizuresViewSet(viewsets.ModelViewSet):
    """API endpoint for seizures."""
    queryset = Seizure.objects.all()
    serializer_class = SeizureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = "__all__"


class SeizuresErrorView(TemplateView):
    """Error handlers template view shows message with status code."""
    message = "Sorry, but unfortunately, there was an unknown error."
    status_code = 500
    template_name = "seizures.html"

    def dispatch(self, request, *args, **kwargs):
        messages.error(request=request,message=self.message)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=self.status_code)


class SeizuresLoginView(LoginView):
    """Log in view."""
    template_name = "login.html"


class SeizuresLogoutView(LogoutView):
    """Log out view."""
    template_name = "login.html"


class SeizuresBaseView(PermissionRequiredMixin, ListView):
    """Seizures base view."""
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    model = Seizure
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html"

    def get_context_data(self, *args, **kwargs):
        """Include search form, and JSON seizure data, in response context."""
        context = super().get_context_data(*args, **kwargs)

        context["search_form"] = SeizuresSearchDateForm()
        seizures = context.get("seizures")
        if seizures:
            context["seizures"] = serialize(format="json", queryset=seizures)
            if settings.DEVICE_ICONS:
                context["device_icons"] = settings.DEVICE_ICONS

        return context


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

    def get_queryset(self, *args, **kwargs):
        """Filter seizures recorded between datetime values."""
        return super().get_queryset(*args, **kwargs).filter(
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
            max_date=timezone.localtime().strftime(dt_fmt)
        )
        return super().render_to_response(context)


class SeizuresSSIDView(SeizuresBaseView):
    """Search for seizures from a specific SSID network name."""

    def get_queryset(self):
        """Filter seizures from the requested SSID."""
        self.extra_context = {"search_ssid": self.kwargs["search_ssid"]}
        return super().get_queryset().filter(
            ssid__exact=self.kwargs["search_ssid"]
        )
