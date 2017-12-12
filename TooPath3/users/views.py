from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.devices.permissions import IsOwnerOrReadOnly
from TooPath3.models import CustomUser
from TooPath3.users.serializers import CustomUserSerializer, PublicCustomUserSerializer, LoginSerializer
from TooPath3.utils import generate_token_for_user


class UserDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def get(self, request, u_pk):
        user = self.get_object(u_pk)
        serializer = PublicCustomUserSerializer(instance=user)
        return Response(status=HTTP_200_OK, data=serializer.data)

    def patch(self, request, u_pk):
        user = self.get_object(u_pk)
        serializer = CustomUserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            user_updated = serializer.save()
            return Response(data=PublicCustomUserSerializer(user_updated).data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, u_pk):
        user = self.get_object(u_pk)
        serializer = CustomUserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            user_updated = serializer.save()
            return Response(data=PublicCustomUserSerializer(user_updated).data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserList(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user_created = serializer.save()
            return Response(data=PublicCustomUserSerializer(instance=user_created).data, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=serializer.validated_data['email'])
            except CustomUser.DoesNotExist:
                return Response(data=DEFAULT_ERROR_MESSAGES['invalid_email'], status=HTTP_400_BAD_REQUEST)
            if not user.check_password(serializer.validated_data['password']):
                return Response(data=DEFAULT_ERROR_MESSAGES['invalid_password'], status=HTTP_400_BAD_REQUEST)
            response_data = {'token': generate_token_for_user(user)}
            return Response(data=response_data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
