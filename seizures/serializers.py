from django.contrib.auth.models import User, Group

from rest_framework import serializers
from seizures.models import Seizure


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SeizureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seizure
        fields = '__all__'
