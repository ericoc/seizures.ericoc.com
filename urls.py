from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from seizures.views import APIUserViewSet, APISeizureViewSet


api_router = routers.DefaultRouter()
api_router.register(r"users", APIUserViewSet)
api_router.register(r"seizures", APISeizureViewSet)

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/", include(api_router.urls), name="api"),
    path("", include("seizures.urls"), name="seizures")
]
