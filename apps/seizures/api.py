from rest_framework.routers import DefaultRouter

from .views.api import APISeizuresViewSet


api_router = DefaultRouter()
api_router.register(prefix=r"seizures", viewset=APISeizuresViewSet)
