from rest_framework.serializers import ModelSerializer

from .models import Seizure


class SeizureSerializer(ModelSerializer):
    class Meta:
        model = Seizure
        fields = "__all__"
