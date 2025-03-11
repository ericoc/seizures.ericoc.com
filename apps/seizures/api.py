from rest_framework.filters import OrderingFilter
from rest_framework.routers import DefaultRouter
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Seizure


class SeizureSerializer(ModelSerializer):
    """Django-Rest-Framework (DRF) serializer for seizures API endpoint."""
    class Meta:
        model = Seizure
        fields = "__all__"


class APISeizuresViewSet(ModelViewSet):
    """Django-Rest-Framework (DRF) ModelViewSet API endpoint for seizures."""
    filter_backends = (OrderingFilter,)
    filterset_fields = fields = ordering_fields = "__all__"
    model = Seizure
    queryset = model.objects.all()
    serializer_class = SeizureSerializer

api_router = DefaultRouter()
api_router.register(prefix=r"seizures", viewset=APISeizuresViewSet)
