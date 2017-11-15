from rest_framework import serializers

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Device
        fields = '__all__'

    def validate(self, data):
        if self.partial is True:
            if 'pk' in data or 'did' in data:
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_patch'])
            if bool(data) is False or len(self.initial_data) != len(data):
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['patch_device_fields_required'])
        return data
