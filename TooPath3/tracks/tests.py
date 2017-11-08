from django.contrib.auth.hashers import make_password
from rest_framework.status import *
from rest_framework.test import APITestCase, APIClient

from TooPath3.models import CustomUser, Device
from TooPath3.users.utils import generate_token_for_testing


class PostTracksCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='user_test', password=make_password('password'))
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.post('/devices/100/tracks/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_doesnt_have_permissions(self):
        owner = CustomUser.objects.create(username='owner', password=make_password('password'))
        device = Device.objects.create(name='device_test', device_type='ad', device_privacy='pr', owner=owner)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/', {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)
