from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from rest_framework_jwt.settings import api_settings

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.locations.views import *
from TooPath3.models import Device, CustomUser, TrackLocation
from TooPath3.utils import generate_token_for_testing, get_latest_id_inserted, create_user_with_email, \
    create_device_with_owner, create_track_with_device

VALID_DATA_LOCATION = {
    'latitude': 40.0,
    'longitude': 2.0
}
INVALID_DATA_LOCATION = {
    'lat': 40.0,
    'lon': 2.0
}
INVALID_LATITUDE_DATA_LOCATION = {
    'latitude': 400.0,
    'longitude': 2.0
}
INVALID_LONGITUDE_DATA_LOCATION = {
    'latitude': 40.0,
    'longitude': -200.0
}


class GetActualLocation(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(email='test@gmail.com', username='test',
                                              password=make_password('password'))
        self.user2 = CustomUser.objects.create(email='test2@gmail.com', username='test2',
                                               password=make_password('password'))
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)
        payload = jwt_payload_handler(self.user2)
        self.token2 = jwt_encode_handler(payload)
        device = Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr',
                                       owner=self.user, port_number='8080')
        actual_location = ActualLocation.objects.get(device=device.did)
        actual_location.point = Point(30, 1)
        actual_location.save()

    """
    GET /devices/:id/actualLocation
    """

    def test_given_existing_device__when_get_device_actual_location_with_existing_device_id__then_return_ok(self):
        request = self.factory.get('/devices/1/actualLocation', format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_get_device_actual_location_with_no_authentication__then_return_unauthorized(
            self):
        request = self.factory.get('/devices/1/actualLocation', format='json')
        response = DeviceActualLocation.as_view()(request, pk=1)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_given_existing_device__when_get_device_actual_location_with_non_existing_device_id__then_return_not_found(
            self):
        request = self.factory.get('/devices/1/actualLocation', format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=100)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_get_device_actual_location_with_existing_device_id__then_return_actual_location(
            self):
        request = self.factory.get('/devices/1/actualLocation', format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=1)
        response.render()
        expected_response_content = b'{"id":1,"type":"Feature","geometry":{"type":"Point","coordinates":[30.0,1.0]}'
        self.assertIn(expected_response_content, response.content)


class PutActualLocation(APITestCase):
    """
    PUT /devices/:id/actualLocation
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(email='test@gmail.com', username='test',
                                              password=make_password('password'))
        self.user2 = CustomUser.objects.create(email='test2@gmail.com', username='test2',
                                               password=make_password('password'))
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)
        payload = jwt_payload_handler(self.user2)
        self.token2 = jwt_encode_handler(payload)
        device = Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr',
                                       owner=self.user, port_number='8080')
        actual_location = ActualLocation.objects.get(device=device.did)
        actual_location.point = Point(30, 1)
        actual_location.save()

    def test_given_existing_device__when_put_device_actual_location_with_existing_device_id__then_return_ok(self):
        request = self.factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_put_device_actual_location_with_invalid_data__then_return_bad_request(self):
        request = self.factory.put('/devices/1/actualLocation', INVALID_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=1)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_existing_device__when_put_device_actual_location_with_no_authentication__then_return_unauthorized(
            self):
        request = self.factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        response = DeviceActualLocation.as_view()(request, id=1)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_given_existing_device__when_put_device_actual_location_with_user_logged_different_than_device_owner__then_return_no_permission(
            self):
        request = self.factory.put('/devices/1', VALID_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user2, token=self.token2)
        response = DeviceActualLocation.as_view()(request, pk=1)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_given_existing_device__when_put_device_actual_location_with_invalid_device_id__then_return_not_found(self):
        request = self.factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=100)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_put_device_actual_location_with_valpk_device_id_and_valid_data__then_update_latitude(
            self):
        request = self.factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        DeviceActualLocation.as_view()(request, pk=1)
        actual_location = ActualLocation.objects.get(pk=1)
        self.assertEqual(actual_location.point.x, 40.0)

    def test_given_existing_device__when_put_device_actual_location_with_valid_device_id_and_valid_data__then_update_longitude(
            self):
        request = self.factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        DeviceActualLocation.as_view()(request, pk=1)
        actual_location = ActualLocation.objects.get(pk=1)
        self.assertEqual(actual_location.point.y, 2.0)

    def test_given_existing_device__when_put_device_actual_location_with_invalid_latitude__then_return_latitude_validation_error(
            self):
        request = self.factory.put('/devices/1/actualLocation', INVALID_LATITUDE_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=1)
        self.assertEqual(response.data, {'non_field_errors': ['Enter a valid latitude.']})

    def test_given_existing_device__when_put_device_actual_location_with_invalid_latitude__then_return_longitude_validation_error(
            self):
        request = self.factory.put('/devices/1/actualLocation', INVALID_LONGITUDE_DATA_LOCATION, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = DeviceActualLocation.as_view()(request, pk=1)
        self.assertEqual(response.data, {'non_field_errors': ['Enter a valid longitude.']})


class PostTrackLocationCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('user_test')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_when_device_not_exists(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.post('/devices/100/tracks/' + str(track.tid) + '/trackLocations/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_404_when_track_not_exists(self):
        device = create_device_with_owner(self.user)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/100/trackLocations/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post('/devices/100/tracks/100/trackLocations/', {})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_email('owner')
        device = create_device_with_owner(owner)
        track = create_track_with_device(device)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/trackLocations/',
                                    {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_201_status_when_track_location_created(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        json_body = {'point': {'type': 'Point', 'coordinates': [90, 90]}}
        response = self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/trackLocations/',
                                    json_body)
        self.assertEqual(HTTP_201_CREATED, response.status_code)

    def test_instance_exists_status_when_track_location_created(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        json_body = {'point': {'type': 'Point', 'coordinates': [90, 90]}}
        self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/trackLocations/',
                         json_body)
        track_location = self._get_track_location_by_id(get_latest_id_inserted(TrackLocation))
        self.assertIsNotNone(track_location)

    def test_return_json_with_instance_info_status_when_track_location_created(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        json_body = {'point': {'type': 'Point', 'coordinates': [90, 90]}}
        response = self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/trackLocations/',
                                    json_body)
        expected_json = TrackLocationSerializer(
            self._get_track_location_by_id(get_latest_id_inserted(TrackLocation))).data
        self.assertEqual(expected_json, response.data)

    def test_return_invalid_latitude_error_when_body_has_invalid_latitude(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        json_body = {'point': {'type': 'Point', 'coordinates': [91, 90]}}
        response = self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/trackLocations/',
                                    json_body)
        expected_json = {'non_field_errors': [DEFAULT_ERROR_MESSAGES['invalid_latitude']]}
        self.assertEqual(expected_json, response.data)

    def test_return_invalid_longitude_error_when_body_has_invalid_longitude(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        json_body = {'point': {'type': 'Point', 'coordinates': [1, 181]}}
        response = self.client.post('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/trackLocations/',
                                    json_body)
        expected_json = {'non_field_errors': [DEFAULT_ERROR_MESSAGES['invalid_longitude']]}
        self.assertEqual(expected_json, response.data)

    def _get_track_location_by_id(self, id):
        return TrackLocation.objects.get(pk=id)
