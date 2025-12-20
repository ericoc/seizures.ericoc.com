from rest_framework.filters import OrderingFilter
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS
from rest_framework.routers import DefaultRouter
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Seizure


"""
Serializers.
"""

class SeizureSerializer(ModelSerializer):
    """Django-Rest-Framework (DRF) serializer for seizures API endpoint."""
    class Meta:
        model = Seizure
        fields = "__all__"

class PublicSeizureSerializer(SeizureSerializer):
    """Django-Rest-Framework (DRF) serializer for public seizures API endpoint."""
    class Meta:
        model = Seizure
        fields = ("timestamp",)

"""
ViewSets.
"""

""""Base API ViewSet class."""
class BaseAPISeizuresViewSet(ModelViewSet):
    """Django-Rest-Framework (DRF) ModelViewSet base API endpoint for seizures."""
    filter_backends = (OrderingFilter,)
    filterset_fields = fields = ordering_fields = "__all__"
    model = Seizure
    permission_classes = (IsAdminUser,)
    queryset = model.objects.all()

"""Admin ViewSet."""
class APISeizuresViewSet(BaseAPISeizuresViewSet):
    """Django-Rest-Framework (DRF) ModelViewSet API endpoint for seizures."""
    filterset_fields = fields = ordering_fields = "__all__"
    serializer_class = SeizureSerializer

    def get_queryset(self):
        """Optionally filter queryset by device type (?device_type=iPhone)."""
        qs = super().get_queryset()

        device_type = self.request.query_params.get("device_type")
        if device_type is not None:
            qs = qs.filter(device_type__exact=device_type)

        return qs

"""Public ViewSet (ReadOnly)."""
class ReadOnly(BasePermission):
    """Create read-only permission class for class PublicAPISeizuresViewSet."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class PublicAPISeizuresViewSet(BaseAPISeizuresViewSet):
    """Django-Rest-Framework (DRF) ModelViewSet public API endpoint for seizures."""
    filterset_fields = fields = ordering_fields = ("timestamp",)
    permission_classes = (ReadOnly,)
    serializer_class = PublicSeizureSerializer

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


"""Create API router, and endpoints."""
api_router = DefaultRouter()
api_router.register(prefix=r"seizures", viewset=APISeizuresViewSet, basename="seizures")
api_router.register(prefix=r"public", viewset=PublicAPISeizuresViewSet, basename="public")
