from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from TooPath3.locations.serializers import CoordinatesSerializer, ActualLocationSerializer
from TooPath3.models import ActualLocation


class DeviceActualLocation(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        actual_location = get_object_or_404(ActualLocation, pk=pk)
        serializer = ActualLocationSerializer(actual_location)
        if serializer.is_valid:
            return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        actual_location = get_object_or_404(ActualLocation, pk=pk)
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
                return Response(HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
