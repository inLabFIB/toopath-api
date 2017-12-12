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
        self.token = generate_token_for_user(user=self.user)
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


class PatchDeviceCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('user_test')
        self.token = generate_token_for_user(self.user)
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


class PutDeviceCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('user_test')
        self.token = generate_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_found(self):
        response = self.client.put(path='/devices/10/', data={}, format='json')
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_email(email='owner@gmail.com')
        device = create_device_with_owner(owner=owner)
        response = self.client.put(path='/devices/' + str(device.did) + '/', data={}, format='json')
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.put(path='/devices/1/', data={}, format='json')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        device = create_device_with_owner(owner=self.user)
        json_body = {"device_name": "test", "ip_address": "127.0.0.1"}
        response = self.client.put(path='/devices/' + str(device.did) + '/', data=json_body, format='json')
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_return_200_status_when_put_device_is_done(self):
        device = create_device_with_owner(owner=self.user)
        json_body = {"name": "test", "ip_address": "127.0.0.1"}
        response = self.client.put(path='/devices/' + str(device.did) + '/', data=json_body, format='json')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_data_when_put_device_is_done(self):
        device = create_device_with_owner(owner=self.user)
        json_body = {"name": "test", "ip_address": "127.0.0.1"}
        response = self.client.put(path='/devices/' + str(device.did) + '/', data=json_body, format='json')
        device_updated = Device.objects.get(pk=device.did)
        self.assertEqual(DeviceSerializer(device_updated).data, response.data)

    def test_check_instance_modified_when_put_device_is_done(self):
        device = create_device_with_owner(owner=self.user)
        json_body = {"name": "test", "ip_address": "127.0.0.1"}
        self.client.put(path='/devices/' + str(device.did) + '/', data=json_body, format='json')
        device_updated = Device.objects.get(pk=device.did)
        expected_ip_address = "127.0.0.1"
        self.assertEqual(expected_ip_address, device_updated.ip_address)


class GetDevicesCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('test@gmail.com')
        self.token = generate_token_for_user(self.user)
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

    def test_return_json_response_when_get_devices_done(self):
        create_various_devices_with_owner(self.user)
        different_owner = create_user_with_email('new@gmai.l.com')
        create_device_with_owner(different_owner)
        response = self.client.get(path='/devices/')
        devices = Device.objects.filter(owner=self.user)
        self.assertEqual(DeviceSerializer(devices, many=True).data, response.data)


class PostDeviceCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('test@gmail.com')
        self.token = generate_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_401_status_when_user_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(path='/devices/', data={}, format='json')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        json_body = {"device_name": "test", "device_type": "ad", "device_privacy": "pr"}
        response = self.client.post(path='/devices/', data=json_body, format='json')
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_return_201_status_when_post_device_is_done(self):
        json_body = {"name": "test"}
        response = self.client.post(path='/devices/', data=json_body, format='json')
        self.assertEqual(HTTP_201_CREATED, response.status_code)

    def test_instance_created_when_post_device_is_done(self):
        json_body = {"name": "test"}
        self.client.post(path='/devices/', data=json_body, format='json')
        device_created = Device.objects.get(pk=get_latest_id_inserted(Device))
        self.assertIsNotNone(device_created)

    def test_return_json_response_when_post_device_is_done(self):
        json_body = {"name": "test"}
        response = self.client.post(path='/devices/', data=json_body, format='json')
        device_created = Device.objects.get(pk=get_latest_id_inserted(Device))
        self.assertEqual(DeviceSerializer(instance=device_created).data, response.data)

    def test_owner_in_json_response_when_post_device_is_done(self):
        json_body = {"name": "test"}
        response = self.client.post(path='/devices/', data=json_body, format='json')
        self.assertEqual(self.user.username, response.data['owner'])

    def test_token_corresponds_with_owner_in_json_response_when_post_is_done(
            self):
        json_body = {"name": "test"}
        response = self.client.post(path='/devices/', data=json_body, format='json')
        payload = jwt_decode_handler(self.token)
        username = jwt_get_username_from_payload(payload)
        self.assertEqual(response.data['owner'], username)
