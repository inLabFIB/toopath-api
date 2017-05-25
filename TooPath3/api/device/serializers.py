from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from TooPath3.api.device.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.api.models import Location, Device


class DeviceLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(source='extract_latitude_point', read_only='True')
    longitude = serializers.FloatField(source='extract_longitude_point', read_only='True')

    class Meta:
        model = Device
        fields = ('latitude', 'longitude')


class DeviceIpAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('ip_address',)


class LocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Location
        geo_field = 'location'
        fields = ('did', 'latitude', 'longitude')

    def validate(self, data):
        if (data['location'].x < -90.0) or (data['location'].x > 90.0):
            raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_latitude'])
        elif (data['location'].y < -180) or (data['location'].y > 180):
            raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_longitude'])
        return data


class LocationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')

    def validate(self, data):
        if ('latitude' not in data) or ('longitude' not in data):
            raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_format'])
        return data
