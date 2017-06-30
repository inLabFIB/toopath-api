from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *

from TooPath3.location.serializers import CoordinatesSerializer, ActualLocationSerializer
from TooPath3.models import Device


@api_view(['POST'])
def device_location(request, id):
    device = get_object_or_404(Device, pk=id)
    data = JSONParser().parse(request)
    serializer = CoordinatesSerializer(data=data)
    if serializer.is_valid():
        geo_json = {
            'device': device.did,
            'location': {
                'type': 'Point',
                'coordinates': [serializer.validated_data['latitude'], serializer.validated_data['longitude']]
            }
        }
        serializer = ActualLocationSerializer(data=geo_json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
