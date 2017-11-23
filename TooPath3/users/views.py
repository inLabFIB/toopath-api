from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from TooPath3.devices.permissions import IsOwnerOrReadOnly
from TooPath3.models import CustomUser
from TooPath3.users.serializers import CustomUserSerializer


class UserDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def get(self, request, u_pk):
        user = self.get_object(u_pk)
        return Response(status=HTTP_200_OK)


@api_view(['POST'])
def new_user(request):
    data = JSONParser().parse(request)
    serializer = CustomUserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = {
            'token': jwt_encode_handler(payload)
        }
        return Response(token, HTTP_201_CREATED)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)
