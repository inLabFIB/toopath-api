from django.contrib.auth.hashers import make_password
from rest_framework_jwt.settings import api_settings

from TooPath3.models import CustomUser, Device, Track


def get_jwt_secret(user):
    custom_user = CustomUser.objects.get(pk=user.pk)
    return custom_user.jwt_secret


def generate_token_for_testing(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def get_latest_id_inserted(model_class):
    return model_class.objects.latest('pk').pk


def _create_user_with_username(username):
    return CustomUser.objects.create(username=username, password=make_password('password'))


def _create_device_with_owner(owner):
    return Device.objects.create(name='device_test', device_type='ad', device_privacy='pr', owner=owner)


def create_track(device):
    return Track.objects.create(name='track_test', device=device)
