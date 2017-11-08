from django.contrib.auth.hashers import make_password
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.test import APITestCase, APIClient

from TooPath3.models import CustomUser
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
