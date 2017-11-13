from rest_framework import serializers

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

    def validate(self, data):
        if self.partial is True:
            if 'device' in data:
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_patch'])
            elif 'description' in data or 'name' in data:
                return data
            else:
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['patch_track_fields_required'])
        return data
