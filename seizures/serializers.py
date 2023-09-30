from django.contrib.auth.models import User, Group
from rest_framework import serializers

from seizures.models import Seizure


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class SeizureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seizure
        fields = "__all__"
