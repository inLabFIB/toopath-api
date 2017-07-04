from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from TooPath3.devices.serializers import DeviceSerializer
from TooPath3.models import Device


@api_view(['GET'])
def device(request, id):
    if request.method == 'GET':
        device = get_object_or_404(Device, pk=id)
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=HTTP_200_OK)
