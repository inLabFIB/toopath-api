from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from TooPath3.devices.permissions import IsOwnerOrReadOnly
from TooPath3.models import Device
from TooPath3.tracks.serializers import TrackSerializer


class TrackList(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Device, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def post(self, request, pk):
        device = self.get_object(pk)
        request.data['device'] = device.did
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            track = serializer.save()
            track_json = TrackSerializer(track).data
            return Response(track_json, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TrackDetail(APIView):
    def get_object(self, pk, model_class):
        obj = get_object_or_404(model_class, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def post(self, request, d_pk, t_pk):
        self.get_object(d_pk, Device)
