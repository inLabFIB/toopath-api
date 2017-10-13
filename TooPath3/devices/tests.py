from django.contrib.auth.hashers import make_password
from rest_framework.status import *
from rest_framework.test import APITestCase, force_authenticate, APIClient
from rest_framework_jwt.settings import api_settings

from TooPath3.devices.views import DeviceDetail
from TooPath3.models import Device, CustomUser

# DATA CONSTANTS
VALID_DATA_POST_DEVICE = {
    "name": "test",
    "ip_address": "127.0.0.1",
    "port_number": 8000,
    "device_type": "ad",
    "device_privacy": "pr"
}
VALID_DATA_PUT_DEVICE = {
    "ip_address": "127.0.0.1",
    "port_number": 8000
}
INVALID_DATA_PUT_DEVICE = {
    "ip": "127.0.0.1"
}


class DevicesTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='test', password=make_password('password'))
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)
        Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr',
                              port_number='8080', owner=self.user)
        # user2 creation
        self.user2 = CustomUser.objects.create(username='test2', password=make_password('password'))
        payload = jwt_payload_handler(self.user2)
        self.token2 = jwt_encode_handler(payload)

    """ 
    GET /devices/:id
    """

    def test_given_existing_device__when_get_device_with_existing_device_id__then_return_ok(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get('/devices/1/', format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_get_device_with_non_existing_device_id__then_return_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get('/devices/10/', format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    """ 
    PUT /devices/:id
    """

    def test_given_existing_device__when_put_device_with_existing_device_id_and_valid_data__then_return_ok(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.put('/devices/1/', VALID_DATA_PUT_DEVICE, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_put_device_with_non_existing_device_id_and_valid_data__then_return_ok(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.put('/devices/10/', VALID_DATA_PUT_DEVICE, format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_put_device_with_existing_device_id_and_invalid_data__then_return_ok(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.put('/devices/1/', INVALID_DATA_PUT_DEVICE, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_existing_device__when_put_device_with_existing_device_id_and_valid_data__then_return_ip_address(
            self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        self.client.put('/devices/1/', VALID_DATA_PUT_DEVICE, format='json')
        device = Device.objects.get(pk=1)
        self.assertEqual(device.ip_address, '127.0.0.1')

    def test_given_existing_device__when_put_device_with_user_logged_different_than_device_owner__then_return_no_permission(
            self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        response = self.client.put('/devices/1/', VALID_DATA_PUT_DEVICE, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    """
    POST /devices
    """

    def test_given_non_existing_device__when_post_device_with_valid_information__then_return_created_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post('/devices/', VALID_DATA_POST_DEVICE)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_given_non_existing_device__when_post_device_with_invalid_information__then_return_bad_response_status(
            self):
        self.fail()

    def test_given_non_existing_device__when_post_device_with_valid_information__then_check_device_database_entry_exist(
            self):
        self.fail()

    def test_given_non_existing_device__when_post_device_with_valid_information__then_return_device_information_on_response(
            self):
        self.fail()

    def test_given_non_existing_device__when_post_device_with_valid_information__then_owner_corresponds_with_token(
            self):
        self.fail()

    def test_given_non_existing_device__when_post_device_with_invalid_information__then_has_relation_with_actual_location_entry_exist(
            self):
        self.fail()
