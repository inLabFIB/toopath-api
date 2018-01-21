from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point
import requests
from rest_framework_jwt.settings import api_settings
from TooPath3.models import CustomUser, Device, Track, TrackLocation


def get_jwt_secret(user):
    custom_user = CustomUser.objects.get(pk=user.pk)
    return custom_user.jwt_secret


def generate_token_for_user(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def get_latest_id_inserted(model_class):
    return model_class.objects.latest('pk').pk


# Methods for Test Cases

def create_user_with_email(email):
    return CustomUser.objects.create(email=email, username=email.split('@')[0])


def create_device_with_owner(owner):
    return Device.objects.create(name='device_test', device_type='ad', device_privacy='pr', owner=owner)


def create_various_devices_with_owner(owner):
    count = 0
    while count < 5:
        device_instance = create_device_with_owner(owner)
        track_instance = create_track_with_device(device_instance)
        create_various_track_locations_with_track(track_instance)
        count += 1


def create_track_with_device(device):
    return Track.objects.create(name='track_test', device=device)


def create_track_location_with_track(track):
    return TrackLocation.objects.create(point=Point(44, 67), track=track)


def create_various_track_locations_with_track(track):
    count = 0
    while count < 5:
        create_track_location_with_track(track)
        count += 1


def validate_google_token(token):
    params = {'id_token': token}
    return requests.post('https://www.googleapis.com/oauth2/v3/tokeninfo', params=params)


def generate_user_info_from_google(email, name):
    return {'email': email,
            'username': email.split('@')[0],
            'password': make_password(email.split('@')[0]),
            'first_name': name.split()[0],
            'last_name': name.split()[1]}
