from rest_framework.status import *
from rest_framework.test import APITestCase, APIClient

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.models import Track
from TooPath3.tracks.serializers import TrackSerializer
from TooPath3.utils import generate_token_for_testing, create_user_with_username, create_device_with_owner, \
    create_track_with_device, get_latest_id_inserted, create_various_track_locations_with_track


class GetTrackCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_username('user_test')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.get('/devices/100/tracks/1/')
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_404_status_when_track_not_exists(self):
        device = create_device_with_owner(self.user)
        response = self.client.get('/devices/' + str(device.did) + '/tracks/100/')
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get('/devices/1/tracks/1/')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_200_status_when_get_track_is_done(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        create_various_track_locations_with_track(track)
        response = self.client.get('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_with_track_info_when_get_track_is_done(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        create_various_track_locations_with_track(track)
        response = self.client.get('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/')
        self.assertEqual(TrackSerializer(track).data, response.data)


class GetTracksCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_username('user_test')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.get('/devices/100/tracks/')
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_username('owner')
        device = create_device_with_owner(owner)
        response = self.client.get('/devices/' + str(device.did) + '/tracks/', {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get('/devices/1/tracks/')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_200_status_when_get_tracks_is_done(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        create_various_track_locations_with_track(track)
        track2 = create_track_with_device(device)
        create_various_track_locations_with_track(track2)
        response = self.client.get('/devices/' + str(device.did) + '/tracks/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_with_tracks_info_when_get_track_is_done(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        create_various_track_locations_with_track(track)
        track2 = create_track_with_device(device)
        create_various_track_locations_with_track(track2)
        response = self.client.get('/devices/' + str(device.did) + '/tracks/')
        tracks = Track.objects.filter(device=device)
        self.assertEqual(TrackSerializer(tracks, many=True).data, response.data)


class PostTracksCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_username('user_test')
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
        self.client.post('/devices/' + str(device.did) + '/tracks/',
                         {"name": "test_track", "description": "this is a description"})
        track = Track.objects.get(pk=get_latest_id_inserted(Track))
        self.assertIsNotNone(track)

    def test_return_json_with_instance_info_when_track_is_created(self):
        device = create_device_with_owner(self.user)
        response = self.client.post('/devices/' + str(device.did) + '/tracks/',
                                    {"name": "test_track", "description": "this is a description"})
        track_created = Track.objects.get(pk=get_latest_id_inserted(Track))
        self.assertEqual(TrackSerializer(track_created).data, response.data)


class PatchTrackCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_username('user_test')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.patch('/devices/100/tracks/1/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_404_status_when_track_not_exists(self):
        device = create_device_with_owner(self.user)
        response = self.client.patch('/devices/' + str(device.did) + '/tracks/100/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_username('owner')
        device = create_device_with_owner(owner)
        track = create_track_with_device(device)
        response = self.client.patch('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/', {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.patch('/devices/1/tracks/1/', {})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.patch('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                                     {"desc": "this attribute does not exist"})
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_return_200_status_when_track_updated(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.patch('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                                     {"description": "new description"})
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_instance_updated_status_when_track_updated(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        self.client.patch('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/', {"name": "new_name"})
        track_updated = Track.objects.get(pk=get_latest_id_inserted(Track))
        self.assertEqual("new_name", track_updated.name)

    def test_return_json_with_instance_info_when_track_is_updated(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.patch('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                                     {"name": "new_name"})
        track_updated = Track.objects.get(pk=get_latest_id_inserted(Track))
        self.assertEqual(TrackSerializer(track_updated).data, response.data)

    def test_return_method_error_message_when_try_to_change_instance_representation(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.patch('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                                     {"device": device.did})
        self.assertEqual({'non_field_errors': [DEFAULT_ERROR_MESSAGES['invalid_patch']]}, response.data)


class PutTrackCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_username('user_test')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_device_not_exists(self):
        response = self.client.put('/devices/100/tracks/1/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_404_status_when_track_not_exists(self):
        device = create_device_with_owner(self.user)
        response = self.client.put('/devices/' + str(device.did) + '/tracks/100/', {})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_has_not_permissions(self):
        owner = create_user_with_username('owner')
        device = create_device_with_owner(owner)
        track = create_track_with_device(device)
        response = self.client.put('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/', {})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.put('/devices/1/tracks/1/', {})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.put('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/', {"devices": 3})
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_return_200_status_when_track_updated(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        device2 = create_device_with_owner(self.user)
        response = self.client.put('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                                   {"name": "new_name", "device": device2.did})
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_instance_updated_status_when_track_updated(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        self.client.put('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                        {"name": "new_name", "device": device.did})
        track_updated = Track.objects.get(pk=get_latest_id_inserted(Track))
        self.assertEqual("new_name", track_updated.name)

    def test_return_json_with_instance_info_when_track_is_updated(self):
        device = create_device_with_owner(self.user)
        track = create_track_with_device(device)
        response = self.client.put('/devices/' + str(device.did) + '/tracks/' + str(track.tid) + '/',
                                   {"name": "new_name", "device": device.did})
        track_updated = Track.objects.get(pk=get_latest_id_inserted(Track))
        self.assertEqual(TrackSerializer(track_updated).data, response.data)
