from rest_framework.status import *
from rest_framework.test import APITestCase, APIClient
from rest_framework_jwt.serializers import jwt_decode_handler, jwt_get_username_from_payload

from TooPath3.devices.serializers import DeviceSerializer
from TooPath3.models import ActualLocation

from TooPath3.utils import *

VALID_DATA_POST_DEVICE = {
    "name": "test",
    "ip_address": "127.0.0.1",
    "port_number": 8000,
    "device_type": "ad",
    "device_privacy": "pr"
}
INVALID_DATA_POST_DEVICE = {
    "nam": "test",
    "privacy": "pr"
}
VALID_DATA_PUT_DEVICE = {
    "ip_address": "127.0.0.1",
    "port_number": 8000
}
INVALID_DATA_PUT_DEVICE = {
    "naa": "name"
}


class GetDeviceCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email(email='user@gmail.com')
        self.token = generate_token_for_testing(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_is_not_found(self):
        response = self.client.get(path='/devices/100/', format='json')
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_401_status_when_user_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        device = create_device_with_owner(owner=self.user)
        response = self.client.get(path='/devices/' + str(device.did) + '/', format='json')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_403_status_when_user_is_not_the_device_owner(self):
        different_owner = create_user_with_email(email='diff@gmail.com')
        device = create_device_with_owner(owner=different_owner)
        response = self.client.get(path='/devices/' + str(device.did) + '/', format='json')
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_200_status_when_get_device_is_done(self):
        device = create_device_with_owner(owner=self.user)
        response = self.client.get(path='/devices/' + str(device.did) + '/', format='json')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_data_status_when_get_device_is_done(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        create_various_track_locations_with_track(track)
        response = self.client.get('/devices/' + str(device.did) + '/', format='json')
        self.assertEqual(DeviceSerializer(device).data, response.data)


class PatchDevice(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('user_test')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.patch('/devices/100/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.patch('/devices/1/')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_email('owner')
        device = create_device_with_owner(owner)
        response = self.client.patch('/devices/' + str(device.did) + '/', {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        device = create_device_with_owner(self.user)
        response = self.client.patch('/devices/' + str(device.did) + '/', {"description": "new", "port_num": 0})
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)


class PutDevice(APITestCase):
    """
    PUT /devices/:id
    """

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='test@gmail.com', username='test',
                                              password=make_password('password'))
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)
        Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr',
                              port_number='8080', owner=self.user)
        # user2 creation
        self.user2 = CustomUser.objects.create(email='test2@gmail.com', username='test2', password=make_password(
            'password'))
        payload = jwt_payload_handler(self.user2)
        self.token2 = jwt_encode_handler(payload)

    def test_given_existing_device__when_put_device_with_existing_device_id_and_valid_data__then_return_ok(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.put('/devices/1/', VALID_DATA_PUT_DEVICE, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_put_device_with_non_existing_device_id_and_valid_data__then_return_ok(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.put('/devices/10/', VALID_DATA_PUT_DEVICE, format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

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


class GetDevicesCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('test@gmail.com')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_401_when_user_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(path='/devices/')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_200_when_get_devices_done(self):
        create_various_devices_with_owner(self.user)
        different_owner = create_user_with_email('new@gmai.l.com')
        create_device_with_owner(different_owner)
        response = self.client.get(path='/devices/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_data_when_get_devices_done(self):
        create_various_devices_with_owner(self.user)
        different_owner = create_user_with_email('new@gmai.l.com')
        create_device_with_owner(different_owner)
        response = self.client.get(path='/devices/')
        devices = Device.objects.filter(owner=self.user)
        self.assertEqual(DeviceSerializer(devices, many=True).data, response.data)


class PostDevice(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='test', password=make_password('password'))
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

    def test_given_non_existing_device__when_post_device_with_valid_information__then_return_created_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post('/devices/', VALID_DATA_POST_DEVICE)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_given_non_existing_device__when_post_device_with_invalid_information__then_return_bad_response_status(
            self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post('/devices/', INVALID_DATA_POST_DEVICE)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_non_existing_device__when_post_device_with_valid_information__then_check_device_database_entry_exist(
            self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post('/devices/', VALID_DATA_POST_DEVICE)
        device = Device.objects.get(pk=response.data['did'])
        self.assertIsNotNone(device)

    def test_given_non_existing_device__when_post_device_with_valid_information__then_return_device_information_on_response(
            self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post('/devices/', VALID_DATA_POST_DEVICE)
        self.assertEqual(response.data['owner'], 'test')

    def test_given_non_existing_device__when_post_device_with_valid_information__then_owner_corresponds_with_token(
            self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post('/devices/', VALID_DATA_POST_DEVICE)
        payload = jwt_decode_handler(self.token)
        username = jwt_get_username_from_payload(payload)
        self.assertEqual(response.data['owner'], username)

    def test_given_non_existing_device__when_post_device_with_valid_information__then_has_relation_with_actual_location_entry_exist(
            self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post('/devices/', VALID_DATA_POST_DEVICE)
        device = Device.objects.get(pk=response.data['did'])
        self.assertIsInstance(device.actuallocation, ActualLocation)
