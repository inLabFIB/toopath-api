from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from TooPathAPI.devices.serializer import LocationSerializer, DeviceLocationSerializer
from TooPathAPI.models import Device


@api_view(['GET'])
def last_location(request, id):
    device = get_object_or_404(Device, pk=id)
    data = DeviceLocationSerializer(data=device)
    return Response({'latitude': device.location.x, 'longitude': device.location.y})


@api_view(['POST'])
def post_location(request, id):
    device = get_object_or_404(Device, pk=id)
    data = JSONParser().parse(request)
    data['did'] = int(id)
    serializer = LocationSerializer(data=data)
    if (serializer.is_valid()):
        device.location.x = serializer.validated_data['latitude']
        device.location.y = serializer.validated_data['longitude']
        device.save()
    return Response(status=HTTP_201_CREATED)