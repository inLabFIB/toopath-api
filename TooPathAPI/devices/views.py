from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from TooPathAPI.models import Device


@api_view(['GET'])
def last_location(request, id):
    device = get_object_or_404(Device, pk=id)
    return Response({'latitude': device.location.x, 'longitude': device.location.y})
