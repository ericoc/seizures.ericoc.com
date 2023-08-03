from django.contrib.auth.models import User, Group
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView
from django.views.generic.dates import (
    DateDetailView,
    DayArchiveView,
    MonthArchiveView,
    TodayArchiveView,
    YearArchiveView
)
from rest_framework import permissions, viewsets

from .models import Seizure
from .serializers import UserSerializer, GroupSerializer, SeizureSerializer
from settings import GOOGLEMAPS_API_KEY

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


class SeizureMapView(View):
    """
    Seizures map view.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        latitudes = []
        longitudes = []
        seizures = Seizure.objects.all()[:100]

        for seizure in seizures:
            latitudes.append(seizure.latitude)
            longitudes.append(seizure.longitude)

        return render(
            request=request,
            template_name='map.html.djt',
            context={
                'center_lat': sum(latitudes) / len(latitudes),
                'center_lng': sum(longitudes) / len(longitudes),
                'googlemaps_api_key': GOOGLEMAPS_API_KEY,
                'min_lat': min(latitudes), 'min_lng': min(longitudes),
                'max_lat': max(latitudes), 'max_lng': max(longitudes),
                'seizures': seizures,
                'total_seizures': len(seizures)
            }
        )


class SeizureAddView(View):
    """
    Seizures add view.
    """
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):

        if not request.META.get('CONTENT_TYPE').lower() == 'application/json':
            raise SuspiciousOperation('Invalid content-type.')

        return super(SeizureAddView, self). \
            dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        seizure = Seizure()
        seizure.from_request(request)
        seizure.save()

        return HttpResponse(content='OK', content_type='text/plain')


class SeizureListView(ListView):
    """
    Seizures list all paginated view.
    """
    paginate_by = 15
    model = Seizure
    template_name = 'seizures.html.djt'
    context_object_name = 'seizures'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.paginate_by = request.GET.get('per_page', self.paginate_by)
        return super().get(request, *args, **kwargs)


class SeizureTodayView(TodayArchiveView):
    """
    Seizure view for the current day.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    model = Seizure
    template_name = 'map.html.djt'


class SeizureDayView(DayArchiveView):
    """
    Seizure detail view for a specific day.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    make_object_list = True
    model = Seizure
    template_name = 'map.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        context = super().get_context_data(*args, **kwargs)
        seizures = context.get('seizures')
        if seizures and len(seizures) > 0:
            context['total_seizures'] = len(seizures)
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


class SeizureBaseView(View):
    """
    Seizure base view.
    """
    pass


class SeizureMonthView(MonthArchiveView):
    """
    Seizure view for a month.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    model = Seizure
    template_name = 'map.html.djt'


class SeizureYearView(YearArchiveView):
    """
    Seizure view for a year.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    make_object_list = True
    model = Seizure
    template_name = 'seizures.html.djt'
