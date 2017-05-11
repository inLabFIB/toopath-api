from TooPathAPI.models import Device
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from TooPath3.TooPathAPI.device import LocationSerializer, DeviceLocationSerializer


@api_view(['GET', 'POST'])
def device_location(request, id):
    if request.method == 'GET':
        device = get_object_or_404(Device, pk=id)
        response = DeviceLocationSerializer(device)
        return Response(response.data)

    elif request.method == 'POST':
        device = get_object_or_404(Device, pk=id)
        data = JSONParser().parse(request)
        data['did'] = int(id)
        serializer = LocationSerializer(data=data)
        if (serializer.is_valid()):
            device.location.x = serializer.validated_data['latitude']
            device.location.y = serializer.validated_data['longitude']
            device.save()
        return Response(status=HTTP_201_CREATED)
