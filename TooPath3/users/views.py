from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework_jwt.settings import api_settings

from TooPath3.users.serializers import UserSerializer


@api_view(['POST'])
def new_user(request):
    data = JSONParser().parse(request)
    if 'password' in data:
        data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
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
