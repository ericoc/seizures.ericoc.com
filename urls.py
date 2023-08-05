from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

import seizures.views.api
import seizures.views.add
import seizures.views.all
import seizures.views.date
import seizures.views.recent


api_router = routers.DefaultRouter()
api_router.register(r'users', seizures.views.api.APIUserViewSet)
api_router.register(r'groups', seizures.views.api.APIGroupViewSet)
api_router.register(r'seizures', seizures.views.api.APISeizureViewSet)

# Automatic URL routing.
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include(api_router.urls), name='api'),
    path('add/', seizures.views.add.SeizureAddView.as_view(), name='add'),
    path('all/', seizures.views.all.SeizureAllView.as_view(), name='all'),
    path('', seizures.views.recent.SeizureRecentView.as_view(), name='index'),
    path(
        '<int:year>/',
        seizures.views.date.SeizureYearView.as_view(),
        name='year'
    ),
    path(
        '<int:year>/<int:month>/',
        seizures.views.date.SeizureMonthView.as_view(),
        name='month'
    ),
    path(
        '<int:year>/<int:month>/<int:day>/',
        seizures.views.date.SeizureDayView.as_view(),
        name='day'
    )
]
