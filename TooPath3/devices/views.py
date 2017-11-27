from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from TooPath3.devices.permissions import IsOwnerOrReadOnly
from TooPath3.devices.serializers import DeviceSerializer
from TooPath3.models import Device, ActualLocation


class DeviceDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(klass=Device, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def get(self, request, d_pk):
        device = self.get_object(pk=d_pk)
        serializer = DeviceSerializer(instance=device)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def patch(self, request, d_pk):
        self.get_object(pk=d_pk)
        serializer = DeviceSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            return Response(status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, d_pk):
        device = self.get_object(pk=d_pk)
        serializer = DeviceSerializer(instance=device, data=request.data)
        if serializer.is_valid():
            device_updated = serializer.save()
            return Response(data=DeviceSerializer(device_updated).data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeviceList(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get(self, request):
        devices = Device.objects.filter(owner=request.user)
        serializer = DeviceSerializer(instance=devices, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
