from rest_framework import serializers

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, data):
        if self.partial is True:
            if 'pk' in data or 'id' in data or 'email' in data or 'username' in data:
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_patch'])
            if bool(data) is False or len(self.initial_data) != len(data):
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['patch_device_fields_required'])
        return data


# Custom User Serializer for GET methods
class PublicCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', 'jwt_secret')
