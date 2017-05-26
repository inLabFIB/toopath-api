from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from TooPath3.api.device.serializers import DeviceLocationSerializer, LocationSerializer, LocationDataSerializer, \
    DeviceIpAddressSerializer
from TooPath3.api.models import Device


@api_view(['GET', 'POST'])
def device_location(request, id):
    device = get_object_or_404(Device, pk=id)

    if request.method == 'GET':
        serializer = DeviceLocationSerializer(device)
        return Response(serializer.data, HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LocationDataSerializer(data=data)
        if serializer.is_valid():
            geo_json = {
                'device': id,
                'location': {
                    'type': 'Point',
                    'coordinates': [serializer.validated_data['longitude'], serializer.validated_data['latitude']],
                }
            }
            serializer = LocationSerializer(data=geo_json)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def device_ip_address(request, id):
    device = get_object_or_404(Device, pk=id)

    if request.method == 'GET':
        serializer = DeviceIpAddressSerializer(device)
        return Response(serializer.data, HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DeviceIpAddressSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
