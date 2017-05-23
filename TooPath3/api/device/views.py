from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from TooPath3.api.device.serializers import DeviceLocationSerializer, LocationSerializer, LocationDataSerializer
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
        if (serializer.is_valid()):
            geo_json = {
                "did": id,
                "latitude": data['latitude'],
                "longitude": data['longitude'],
                "location": {
                    "type": "Point",
                    "coordinates": [data['latitude'], data['longitude']],
                }
            }
            serializer = LocationSerializer(data=geo_json)
            if (serializer.is_valid()):
                device.location.x = serializer.validated_data['latitude']
                device.location.y = serializer.validated_data['longitude']
                device.save()
                serializer.save()
                return Response(serializer.data, HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


@api_view('PUT')
def device_ip_address(request, id):
    device = get_object_or_404(Device, pk=id)
    data = JSONParser().parse(request)
    serializer = IpAddressSerializer(data=data)
    if (serializer.is_valid()):
        return Response(serializer.data, HTTP_200_OK)
    else:
        return Response(status=HTTP_400_BAD_REQUEST)
