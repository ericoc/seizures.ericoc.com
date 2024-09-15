from rest_framework.routers import DefaultRouter
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Seizure


class SeizureSerializer(ModelSerializer):
    """
    Django-Rest-Framework (DRF) serializer for seizures API endpoint.
    """
    class Meta:
        model = Seizure
        fields = "__all__"


class APISeizuresViewSet(ModelViewSet):
    """
    Django-Rest-Framework (DRF) ModelViewSet API endpoint for seizures.
    """
    filterset_fields = fields = "__all__"
    model = Seizure
    queryset = model.objects
    serializer_class = SeizureSerializer


api_router = DefaultRouter()
api_router.register(prefix=r"seizures", viewset=APISeizuresViewSet)
