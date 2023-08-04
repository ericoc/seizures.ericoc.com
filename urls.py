from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

import seizures.views


api_router = routers.DefaultRouter()
api_router.register(r'users', seizures.views.APIUserViewSet)
api_router.register(r'groups', seizures.views.APIGroupViewSet)
api_router.register(r'seizures', seizures.views.APISeizureViewSet)

# Automatic URL routing.
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include(api_router.urls), name='api'),
    path('add/', seizures.views.SeizureAddView.as_view(), name='add'),
    path('all/', seizures.views.SeizureAllView.as_view(), name='all'),
    path('today/', seizures.views.SeizureTodayView.as_view(), name='today'),
    path('', seizures.views.SeizureRecentView.as_view(), name='index'),
    path(
        '<int:year>/',
        seizures.views.SeizureYearView.as_view(),
        name='year'
    ),
    path(
        '<int:year>/<int:month>/',
        seizures.views.SeizureMonthView.as_view(month_format='%m'),
        name='month'
    ),
    path(
        '<int:year>/<int:month>/<int:day>/',
        seizures.views.SeizureDayView.as_view(month_format='%m'),
        name='day'
    )
]
