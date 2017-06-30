from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from TooPath3.devices.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.models import Location, ActualLocation


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class ActualLocationSerializer(gis_serializers.GeoFeatureModelSerializer):
    class Meta:
        model = ActualLocation
        geo_field = 'location'
        fields = ('device',)

    def validate(self, data):
        if (data['location'].y < -90.0) or (data['location'].y > 90.0):
            raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_latitude'])
        elif (data['location'].x < -180) or (data['location'].x > 180):
            raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_longitude'])
        return data
