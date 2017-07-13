from django.contrib.auth.models import User
from rest_framework.status import *
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_jwt.settings import api_settings

from TooPath3.devices.views import device_detail
from TooPath3.models import Device

# DATA CONSTANTS
VALID_DATA_DEVICE = {
    "ip_address": "127.0.0.1"
}
INVALID_DATA_DEVICE = {
    "ip": "127.0.0.1"
}


class DevicesTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='test', password='password')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)
        Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr')

    """ 
    GET /devices/:id
    """

    def test_given_existing_device__when_get_device_with_existing_device_id__then_return_ok(self):
        request = self.factory.get('/devices/1', format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = device_detail(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_get_device_with_non_existing_device_id__then_return_not_found(self):
        factory = APIRequestFactory()
        request = self.factory.get('/devices/1', format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = device_detail(request, id=10)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    """ 
    PUT /devices/:id
    """

    def test_given_existing_device__when_put_device_with_existing_device_id_and_valid_data__then_return_ok(self):
        request = self.factory.put('/devices/1', VALID_DATA_DEVICE, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = device_detail(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_put_device_with_non_existing_device_id_and_valid_data__then_return_ok(self):
        request = self.factory.put('/devices/1', VALID_DATA_DEVICE, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = device_detail(request, id=10)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_put_device_with_existing_device_id_and_invalid_data__then_return_ok(self):
        request = self.factory.put('/devices/1', INVALID_DATA_DEVICE, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = device_detail(request, id=1)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_existing_device__when_put_device_with_existing_device_id_and_valid_data__then_return_ip_address(
            self):
        request = self.factory.put('/devices/1', VALID_DATA_DEVICE, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        device_detail(request, id=1)
        device = Device.objects.get(pk=1)
        self.assertEqual(device.ip_address, '127.0.0.1')
