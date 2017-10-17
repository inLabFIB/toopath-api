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
        obj = get_object_or_404(Device, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def get(self, request, id):
        device = self.get_object(id)
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, id):
        device = self.get_object(id)
        data = JSONParser().parse(request)
        if 'name' not in data:
            data['name'] = device.name
        serializer = DeviceSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class DevicesDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.validated_data, HTTP_201_CREATED)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
