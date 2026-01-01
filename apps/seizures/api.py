from django.utils.timezone import localtime, timedelta
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.routers import APIRootView, DefaultRouter
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Seizure


"""
Serializers.
"""

class SeizureSerializer(ModelSerializer):
    """Django-Rest-Framework (DRF) serializer for API endpoint."""
    class Meta:
        model = Seizure
        fields = "__all__"

class PublicSeizureSerializer(SeizureSerializer):
    """Django-Rest-Framework (DRF) serializer for public API of timestamps."""
    class Meta:
        model = Seizure
        fields = ("timestamp",)

"""
ViewSets.
"""

""""Base API ViewSet class."""
class BaseAPISeizuresViewSet(ModelViewSet):
    """Django-Rest-Framework (DRF) ModelViewSet base API endpoint."""
    filter_backends = (OrderingFilter,)
    filterset_fields = fields = ordering_fields = "__all__"
    model = Seizure
    queryset = model.objects.all()

"""Admin ViewSet."""
class APISeizuresViewSet(BaseAPISeizuresViewSet):
    """All fields."""
    filterset_fields = fields = ordering_fields = "__all__"
    permission_classes = (IsAdminUser,)
    serializer_class = SeizureSerializer

    def get_view_name(self):
        """Update Django-Rest-Framework (DRF) admin view name title."""
        return "Administrative API"

"""Public ViewSet (ReadOnly)."""
class PublicAPISeizuresViewSet(BaseAPISeizuresViewSet):
    """Timestamps older than thirty (30) days."""
    filterset_fields = fields = ordering_fields = ("timestamp",)
    model = Seizure
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = model.objects.filter(
        timestamp__lte=localtime()-timedelta(days=30)
    )
    serializer_class = PublicSeizureSerializer

    def get_view_name(self):
        """Update Django-Rest-Framework (DRF) public view name title."""
        return "Public Timestamps"

# Custom APIRootView to ensure public access
class PublicRootAPISeizuresViewSet(APIRootView):
    """"Django-Rest-Framework (DRF) root API endpoint."""
    permission_classes = (IsAuthenticatedOrReadOnly,)


"""Create API router, and endpoints."""
api_router = DefaultRouter()
api_router.APIRootView = PublicRootAPISeizuresViewSet
api_router.get_api_root_view().cls.__name__ = "Seizures"
api_router.get_api_root_view().cls.__doc__ = "API of seizure data."
api_router.register(prefix=r"public", viewset=PublicAPISeizuresViewSet, basename="public")
api_router.register(prefix=r"seizures", viewset=APISeizuresViewSet, basename="seizures")
