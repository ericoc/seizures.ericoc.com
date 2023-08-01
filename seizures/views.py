from django.contrib.auth.models import User, Group
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse, HttpResponseNotAllowed
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

    def dispatch(self, request, *args, **kwargs):

        if not request.META.get('REQUEST_METHOD').lower() == 'post':
            return HttpResponseNotAllowed(['POST'])

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
    Seizures list view.
    """
    paginate_by = 15
    model = Seizure
    template_name = 'seizures.html.djt'
    context_object_name = 'seizures'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.paginate_by = request.GET.get('per_page', self.paginate_by)
        return super(SeizureListView, self). \
            get(request, *args, **kwargs)


class SeizureTodayView(TodayArchiveView):
    """
    Seizure view for the current day.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    make_object_list = True
    model = Seizure
    template_name = 'seizures.html.djt'


class SeizureDateDetailView(DateDetailView):
    """
    Seizure detail view for a specific date.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    make_object_list = True
    model = Seizure
    template_name = 'seizures.html.djt'


class SeizureDayView(DayArchiveView):
    """
    Seizure detail view for a specific day.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    make_object_list = True
    model = Seizure
    template_name = 'seizures.html.djt'


class SeizureMonthView(MonthArchiveView):
    """
    Seizure view for a month.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    make_object_list = True
    model = Seizure
    template_name = 'seizures.html.djt'


class SeizureYearView(YearArchiveView):
    """
    Seizure view for a year.
    """
    date_field = 'timestamp'
    context_object_name = 'seizures'
    make_object_list = True
    model = Seizure
    template_name = 'seizures.html.djt'
