from rest_framework import serializers

from TooPathAPI.models import Location, Device


class DeviceLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField(source='extract_latitude_point', read_only='True')
    longitude = serializers.FloatField(source='extract_longitude_point', read_only='True')

    class Meta:
        model = Device


class LocationSerializer(serializers.ModelSerializer):
    device_id = serializers.RelatedField(source='did', read_only='True')

    class Meta:
        model = Location
        fields = ('latitude', 'longitude', 'device_id')
