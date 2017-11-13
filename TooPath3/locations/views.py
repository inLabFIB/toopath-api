from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from TooPath3.devices.permissions import IsOwnerOrReadOnly
from TooPath3.locations.serializers import CoordinatesSerializer, ActualLocationSerializer, TrackLocationSerializer
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
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk, model_class):
        obj = get_object_or_404(model_class, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def post(self, request, d_pk, t_pk):
        self.get_object(d_pk, Device)
        track = self.get_object(t_pk, Track)
        request.data['track'] = track.tid
        serializer = TrackLocationSerializer(data=request.data)
        if serializer.is_valid():
            track_location_created = serializer.save()
            return Response(TrackLocationSerializer(track_location_created).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
