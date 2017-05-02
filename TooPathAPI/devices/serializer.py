from rest_framework import serializers

from TooPathAPI.models import Location


class LocationSerializer(serializers.ModelSerializer):
    device_id = serializers.RelatedField(source='did', read_only='True')

    class Meta:
        model = Location
        fields = ('latitude', 'longitude', 'device_id')
