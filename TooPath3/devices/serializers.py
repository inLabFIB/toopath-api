from rest_framework import serializers

from TooPath3.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Device
        fields = '__all__'
