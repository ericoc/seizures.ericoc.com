from rest_framework.viewsets import ModelViewSet

from ..models import Seizure
from ..serializers import SeizureSerializer


class APISeizuresViewSet(ModelViewSet):
    """Django-Rest-Framework (DRF) ModelViewSet API endpoint for seizures."""
    filterset_fields = fields = "__all__"
    model = Seizure
    queryset = model.objects
    serializer_class = SeizureSerializer
