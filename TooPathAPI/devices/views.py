from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from TooPathAPI.models import Location


@api_view(['GET'])
def last_location(request, id)
    location = get_object_or_404(Location, devices_id=id)
    print(location.point)
    return Response(location)