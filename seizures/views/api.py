from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets

from ..models import Seizure
from ..serializers import UserSerializer, GroupSerializer, SeizureSerializer


class APISeizureViewSet(viewsets.ModelViewSet):
    """
    API endpoint for seizures.
    """
    queryset = Seizure.objects.all()
    serializer_class = SeizureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'


class APIGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint for groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class APIUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
