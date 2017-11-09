from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from TooPath3.devices.permissions import IsOwnerOrReadOnly
from TooPath3.locations.serializers import CoordinatesSerializer, ActualLocationSerializer
from TooPath3.models import ActualLocation, Track, Device


class DeviceActualLocation(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(ActualLocation, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def get(self, request, pk):
        actual_location = self.get_object(pk)
        serializer = ActualLocationSerializer(actual_location)
        if serializer.is_valid:
            return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        actual_location = self.get_object(pk)
        data = request.data
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
                return Response(status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TrackLocationList(APIView):
    def get_object(self, pk):
        obj = get_object_or_404(Track, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def post(self, request, d_pk, tl_pk):
        get_object_or_404(Device, d_pk)
        track = self.get_object(tl_pk)
        return Response()
