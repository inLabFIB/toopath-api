from collections import OrderedDict

from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_gis.fields import GeoJsonDict

from TooPath3.locations.views import *
from TooPath3.models import Device

# DATA constants
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


class ActualLocationTests(APITestCase):
    def setUp(self):
        device = Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr')
        device.actual_location.point = Point(30, 1)
        device.actual_location.save()

    """
    GET /devices/:id/actualLocation
    """

    def test_given_existing_device__when_get_device_actual_location_with_existing_device_id__then_return_ok(self):
        factory = APIRequestFactory()
        request = factory.get('/devices/1/actualLocation', format='json')
        response = device_actual_location(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_get_device_actual_location_with_non_existing_device_id__then_return_not_found(
            self):
        factory = APIRequestFactory()
        request = factory.get('/devices/1/actualLocation', format='json')
        response = device_actual_location(request, id=100)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_get_device_actual_location_with_existing_device_id__then_return_actual_location(
            self):
        factory = APIRequestFactory()
        request = factory.get('/devices/1/actualLocation', format='json')
        response = device_actual_location(request, id=1)
        response.render()
        expected_response_content = b'{"id":1,"type":"Feature","geometry":{"type":"Point","coordinates":[30.0,1.0]}'
        self.assertIn(expected_response_content, response.content)

    """
    PUT /devices/:id/actualLocation
    """

    def test_given_existing_device__when_put_device_actual_location_with_existing_device_id__then_return_ok(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        response = device_actual_location(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_put_device_actual_location_with_invalid_data__then_return_bad_request(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', INVALID_DATA_LOCATION, format='json')
        response = device_actual_location(request, id=1)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_existing_device__when_put_device_actual_location_with_invalid_device_id__then_return_not_found(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        response = device_actual_location(request, id=100)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_put_device_actual_location_with_valid_device_id_and_valid_data__then_update_latitude(
            self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        device_actual_location(request, id=1)
        actual_location = ActualLocation.objects.get(pk=1)
        self.assertEqual(actual_location.point.x, 40.0)

    def test_given_existing_device__when_put_device_actual_location_with_valid_device_id_and_valid_data__then_update_longitude(
            self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', VALID_DATA_LOCATION, format='json')
        device_actual_location(request, id=1)
        actual_location = ActualLocation.objects.get(pk=1)
        self.assertEqual(actual_location.point.y, 2.0)

    def test_given_existing_device__when_put_device_actual_location_with_invalid_latitude__then_return_latitude_validation_error(
            self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', INVALID_LATITUDE_DATA_LOCATION, format='json')
        response = device_actual_location(request, id=1)
        self.assertEqual(response.data, {'non_field_errors': ['Enter a valid latitude.']})

    def test_given_existing_device__when_put_device_actual_location_with_invalid_latitude__then_return_longitude_validation_error(
            self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', INVALID_LONGITUDE_DATA_LOCATION, format='json')
        response = device_actual_location(request, id=1)
        self.assertEqual(response.data, {'non_field_errors': ['Enter a valid longitude.']})
