from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from TooPath3.models import Device


@api_view(['GET'])
def device(request, id):
    if request.method == 'GET':
        device = get_object_or_404(Device, pj=id)
