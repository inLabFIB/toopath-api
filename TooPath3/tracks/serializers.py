from rest_framework import serializers

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.locations.serializers import TrackLocationSerializer
from TooPath3.models import Track


class TrackSerializer(serializers.ModelSerializer):
    locations = TrackLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = '__all__'

    def validate(self, data):
        if self.partial is True:
            if 'device' in data or 'pk' in data or 'tid' in data:
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_patch'])
            if bool(data) is False:
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['patch_track_fields_required'])
        return data
