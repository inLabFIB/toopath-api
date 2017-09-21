from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *

from TooPath3.locations.serializers import CoordinatesSerializer, ActualLocationSerializer
from TooPath3.models import ActualLocation


@api_view(['GET', 'PUT'])
def device_actual_location(request, id):
    if request.method == 'GET':
        actual_location = get_object_or_404(ActualLocation, pk=id)
        serializer = ActualLocationSerializer(actual_location)
        if serializer.is_valid:
            return Response(serializer.data, status=HTTP_200_OK)

    elif request.method == 'PUT':
        actual_location = get_object_or_404(ActualLocation, pk=id)
        data = JSONParser().parse(request)
        serializer = CoordinatesSerializer(data=data)
        if serializer.is_valid():
            geo_json = {
                'point': {
                    'type': 'Point',
                    'coordinates': [serializer.validated_data['latitude'], serializer.validated_data['longitude']]
                }
            }
            serializer = ActualLocationSerializer(actual_location, data=geo_json)
            if serializer.is_valid():
                serializer.save()
                return Response(HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
