from django.contrib.auth.hashers import make_password
from rest_framework.status import *
from rest_framework.test import APITestCase, APIClient

from TooPath3.models import CustomUser, Device, Track
from TooPath3.utils import generate_token_for_testing, create_user_with_username, create_device_with_owner, create_track_with_device


class PostTracksCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='user_test', password=make_password('password'))
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.post('/devices/100/tracks/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_username('owner')
        device = create_device_with_owner(owner)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/', {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post('/devices/100/tracks/', {})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        device = create_device_with_owner(self.user)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/', {"description": "name missing"})
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_return_201_status_when_track_is_created(self):
        device = create_device_with_owner(self.user)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/',
                                    {"name": "test_track", "description": "this is a description"})
        self.assertEqual(HTTP_201_CREATED, response.status_code)

    def test_instance_exists_when_track_is_created(self):
        device = create_device_with_owner(self.user)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/',
                                    {"name": "test_track", "description": "this is a description"})
        track = Track.objects.get(pk=response.data['tid'])
        self.assertIsNotNone(track)

    def test_return_json_with_instance_info_when_track_is_created(self):
        device = create_device_with_owner(self.user)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/',
                                    {"name": "test_track", "description": "this is a description"})
        expected_json = {'tid': response.data['tid'], 'name': 'test_track', 'description': "this is a description",
                         "device": device.did}
        self.assertEqual(expected_json, response.data)


class PutTracksCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_username('user_test')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.post('/devices/100/tracks/1/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_404_status_when_track_not_exists(self):
        device = create_device_with_owner(self.user)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/100/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_username('owner')
        device = create_device_with_owner(owner)
        track = create_track_with_device(device)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/', {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post('/devices/1/tracks/1/', {})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                                    {"desc": "this attribute does not exist"})
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
