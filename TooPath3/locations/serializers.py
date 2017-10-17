from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.models import ActualLocation


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class ActualLocationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ActualLocation
        geo_field = 'point'
        fields = '__all__'
        read_only_fields = ('device',)

    def validate(self, data):
        if (data['point'].x < -90.0) or (data['point'].x > 90.0):
            raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_latitude'])
        if (data['point'].y < -180) or (data['point'].y > 180):
            raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_longitude'])
        return data
