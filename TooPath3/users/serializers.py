from rest_framework import serializers

from TooPath3.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


# Custom User Serializer for GET methods
class PublicCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', 'jwt_secret')
