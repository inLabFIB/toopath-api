from rest_framework.decorators import api_view
from rest_framework.response import Response

from TooPathAPI.devices.serializers import LocationSerializer
from TooPathAPI.models import Location


@api_view(['GET'])
def last_location(request, id):
    location = Location.getLatestLocationByDeviceId(id)
