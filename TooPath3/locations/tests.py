from builtins import set

from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from rest_framework_jwt.settings import api_settings

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.locations.views import *
from TooPath3.models import Device, CustomUser, TrackLocation
from TooPath3.utils import generate_token_for_user, get_latest_id_inserted, create_user_with_email, \
    create_device_with_owner, create_track_with_device


class GetActualLocation(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email(email='user_test@gmail.com')
        self.token = generate_token_for_user(user=self.user)
        self.device = create_device_with_owner(owner=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_200_status__when_get_is_done(self):
        response = self.client.get(path='/devices/' + str(self.device.did) + '/actualLocation/', format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_return_401_status__when_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(path='/devices/' + str(self.device.did) + '/actualLocation/', format='json')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_return_404_status__when_device_not_found(self):
        response = self.client.get(path='/devices/100/actualLocation/', format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_return_403_status__when_owner_different_than_user_authenticated(self):
        owner = create_user_with_email(email='owner@gmail.com')
        device = create_device_with_owner(owner=owner)
        response = self.client.get(path='/devices/' + str(device.did) + '/actualLocation/', format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_check_response_data_status__when_get_is_done(self):
        response = self.client.get(path='/devices/' + str(self.device.did) + '/actualLocation/', format='json')
        actual_location = ActualLocation.objects.get(pk=self.device.did)
        self.assertEqual(response.data, ActualLocationSerializer(instance=actual_location).data)


class PutActualLocationCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email(email='user_test@gmail.com')
        self.token = generate_token_for_user(user=self.user)
        self.device = create_device_with_owner(owner=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_200_status__when_put_is_done(self):
        json_body = {'point': {'type': 'Point', 'coordinates': [90, 90]}}
        response = self.client.put(path='/devices/' + str(self.device.did) + '/actualLocation/', data=json_body,
                                   format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_return_400_status__when_json_body_is_invalid(self):
        json_body_invalid = {'location': {'type': 'Point', 'coordinates': [90, 90]}}
        response = self.client.put(path='/devices/' + str(self.device.did) + '/actualLocation/', data=json_body_invalid,
                                   format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_return_401_status__when_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.put(path='/devices/' + str(self.device.did) + '/actualLocation/', data={}, format='json')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_return_403_status__when_owner_is_different_than_user_authenticated(self):
        owner = create_user_with_email(email='owner@gmail.com')
        device = create_device_with_owner(owner=owner)
        response = self.client.put(path='/devices/' + str(device.did) + '/actualLocation/', data={}, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_return_404_status__when_device_not_found(self):
        response = self.client.put(path='/devices/100/actualLocation/', data={}, format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_check_instance_updated__when_put_is_done(self):
        json_body = {'point': {'type': 'Point', 'coordinates': [90, 90]}}
        self.client.put(path='/devices/' + str(self.device.did) + '/actualLocation/', data=json_body,
                        format='json')
        actual_location_updated = ActualLocation.objects.get(pk=self.device.did)
        self.assertEqual(actual_location_updated.point.x, 90)

    def test_check_response_data__when_put_is_done(self):
        json_body = {'point': {'type': 'Point', 'coordinates': [90, 90]}}
        response = self.client.put(path='/devices/' + str(self.device.did) + '/actualLocation/', data=json_body,
                                   format='json')
        actual_location_updated = ActualLocation.objects.get(pk=self.device.did)
        self.assertEqual(response.data, ActualLocationSerializer(instance=actual_location_updated).data)

    def test_return_invalid_latitude_error__when_latitude_in_json_body_is_incorrect(self):
        json_body = {'point': {'type': 'Point', 'coordinates': [-200, 90]}}
        response = self.client.put(path='/devices/' + str(self.device.did) + '/actualLocation/', data=json_body,
                                   format='json')
        self.assertEqual(response.data, {'non_field_errors': ['Enter a valid latitude.']})

    def test_return_invalid_longitude_error__when_longitude_in_json_body_is_incorrect(self):
        json_body = {'point': {'type': 'Point', 'coordinates': [90, -200]}}
        response = self.client.put(path='/devices/' + str(self.device.did) + '/actualLocation/', data=json_body,
                                   format='json')
        self.assertEqual(response.data, {'non_field_errors': ['Enter a valid longitude.']})


class PostTrackLocationCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('user_test')
        self.token = generate_token_for_user(self.user)
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
