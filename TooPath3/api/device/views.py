from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from TooPath3.api.device.serializers import DeviceLocationSerializer, LocationSerializer, LocationDataSerializer
from TooPath3.api.models import Device


@api_view(['GET', 'POST'])
def device_location(request, id):
    if request.method == 'GET':
        device = get_object_or_404(Device, pk=id)
        serializer = DeviceLocationSerializer(device)
        return Response(serializer.data, HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LocationDataSerializer(data=data)
        if (serializer.is_valid()):
            device = get_object_or_404(Device, pk=id)
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
