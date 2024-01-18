from django_filters import (
    FilterSet, DateTimeFromToRangeFilter, rest_framework as filters
)

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from ..models import Seizure
from ..serializers import SeizureSerializer


class APISeizuresViewSet(ModelViewSet):
    """DRF ModelViewSet API endpoint for seizures."""
    filterset_fields = fields = "__all__"
    model = Seizure
    queryset = model.objects
    serializer_class = SeizureSerializer


class SeizureFilter(FilterSet):
    min_date = DateTimeFromToRangeFilter(
        field_name="timestamp",
        lookup_expr="gte"
    )
    max_date = DateTimeFromToRangeFilter(
        field_name="timestamp",
        lookup_expr="lte"
    )

    class Meta:
        model = Seizure
        fields = ["timestamp"]


class HelpTextFilterSet(FilterSet):
    @classmethod
    def filter_for_field(cls, field, field_name, lookup_expr=None):
        f = super(FilterSet, cls).filter_for_field(
            field=field,
            field_name=field_name,
            lookup_expr=lookup_expr
        )
        f.extra['help_text'] = f.help_text
        return f


class APISeizuresListView(ListAPIView):
    """DRF generic ListAPIView endpoint for seizures."""
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HelpTextFilterSet
    filterset_fields = fields = "__all__"

    model = Seizure
    queryset = model.objects
    serializer_class = SeizureSerializer
