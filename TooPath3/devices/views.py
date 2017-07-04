from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *

from TooPath3.devices.serializers import DeviceSerializer
from TooPath3.models import Device


@api_view(['GET', 'PUT'])
def device_detail(request, id):
    device = get_object_or_404(Device, pk=id)

    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        if 'name' not in data:
            data['name'] = device.name
        if 'actual_location' not in data:
            data['actual_location'] = device.actual_location
        serializer = DeviceSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
