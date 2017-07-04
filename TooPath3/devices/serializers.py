from rest_framework import serializers

from TooPath3.locations.serializers import ActualLocationSerializer
from TooPath3.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    actual_location = ActualLocationSerializer()

    class Meta:
        model = Device
        fields = '__all__'
