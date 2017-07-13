from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *

from TooPath3.users.serializers import UserSerializer


@api_view(['POST'])
def new_user(request):
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.validated_data, HTTP_201_CREATED)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)
