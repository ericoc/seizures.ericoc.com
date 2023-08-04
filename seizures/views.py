from datetime import timedelta
from django.contrib.auth.models import User, Group
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView
from django.views.generic.dates import (
    DayArchiveView,
    MonthArchiveView,
    TodayArchiveView,
    YearArchiveView
)
from rest_framework import permissions, viewsets

from .models import Seizure
from .serializers import UserSerializer, GroupSerializer, SeizureSerializer
from settings import GOOGLEMAPS_API_KEY


def seize_context(context=None):

    seizures = context.get('seizures')
    if seizures and len(seizures) > 0:

        context['googlemaps_api_key'] = GOOGLEMAPS_API_KEY

        latitudes = []
        longitudes = []

        for seizure in seizures:
            latitudes.append(seizure.latitude)
            longitudes.append(seizure.longitude)

        context['center_lat'] = sum(latitudes) / len(latitudes)
        context['center_lng'] = sum(longitudes) / len(longitudes)

        context['min_lat'] = min(latitudes)
        context['min_lng'] = min(longitudes)

        context['max_lat'] = max(latitudes)
        context['max_lng'] = max(longitudes)

    return context


class APISeizureViewSet(viewsets.ModelViewSet):
    """
    API endpoint for seizures.
    """
    queryset = Seizure.objects.all()
    serializer_class = SeizureSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = '__all__'


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


class SeizureAddView(View):
    """
    Seizures add view.
    """
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):

        if not request.META.get('CONTENT_TYPE').lower() == 'application/json':
            raise SuspiciousOperation('Invalid content-type.')

        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        seizure = Seizure()
        seizure.from_request(request)
        seizure.save()

        return HttpResponse(content='OK', content_type='text/plain')


class SeizureAllView(ListView):
    """
    Seizures list all paginated view.
    """
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    paginate_by = 10
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureTodayView(TodayArchiveView):
    """
    Seizure view for the current day.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureYearView(YearArchiveView):
    """
    Seizure paginated view for a specific year.
    """
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    make_object_list = True
    model = Seizure
    paginate_by = 10
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureMonthView(MonthArchiveView):
    """
    Seizure paginated view for a specific month.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    paginate_by = 10
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureDayView(DayArchiveView):
    """
    Seizure view for a specific day.
    """
    allow_empty = True
    allow_future = False
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureRecentView(ListView):
    """
    Seizure paginated list view for the most recent 24 hours.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    paginate_by = 10
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            timestamp__gte=timezone.now() - timedelta(days=1)
        )
