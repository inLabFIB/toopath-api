from django.contrib.gis.geos import Point
from django.core.serializers import json
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.api.device.views import device_location, device_ip_address
from TooPath3.api.models import Device, Location

# URI constants
DEVICE_URI = '/devices/'
DEVICE_ID_URI = '1'
NON_EXISTENT_DEVICE_ID_URI = '666'
LOCATION_URI = '/location'
IP_ADDRESS_URI = '/ipAddress'

# DATA constants
DATA_LOCATION = {
    "latitude": 40.1234,
    "longitude": 2.1234
}
INVALID_DATA_LOCATION = {
}
INVALID_DATA_IP_ADDRESS = {
    "AA": 1
}
GEO_JSON_RESPONSE_DATA_POST_LOCATION = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [40.1234, 2.1234]
    },
    "properties": {
        "did": 1,
        "latitude": 40.1234,
        "longitude": 2.1234
    }
}
DEVICE_ID = 1
NON_EXISTENT_DEVICE_ID = 666


class DeviceTests(APITestCase):
    def setUp(self):
        Device.objects.create(did=1, name='car', location=Point(40.1234, 2.1234), ip_address='0.0.0.0',
                              device_type='ad', device_privacy='pr')

    """
    GET devices/:id/location
    """

    def test_given_existing_device__when_get_device_location__with_existing_device_id__then_return_ok(self):
        """
        Ensure we get a OK status when get the location from a device
        """
        factory = APIRequestFactory()
        request = factory.get(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI)
        response = device_location(request, id=DEVICE_ID)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_get_device_location__with_non_existent_device_id__then_return_not_found(self):
        """
        Ensure we get a NOT FOUND when pass a non existent device id on request
        """
        factory = APIRequestFactory()
        request = factory.get(DEVICE_URI + NON_EXISTENT_DEVICE_ID_URI + LOCATION_URI)
        response = device_location(request, id=NON_EXISTENT_DEVICE_ID)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_get_device_location__with_existing_device_id__then_return_latitude_and_longitude(
            self):
        """
        Ensure we can get the location from a device
        """
        factory = APIRequestFactory()
        request = factory.get(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI)
        response = device_location(request, id=DEVICE_ID)
        self.assertEqual(response.data, DATA_LOCATION)

    def test_given_existing_device__when_post_device_location_with_existing_device_id__then_return_created(self):
        """
        Ensure we get a CREATED on post device location with existing id
        """
        factory = APIRequestFactory()
        request = factory.post(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI, DATA_LOCATION, format='json')
        response = device_location(request, id=DEVICE_ID)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    """
    POST /devices/:id/location
    """

    def test_given_existing_device__when_post_device_location_with_invalid_data__then_return_bad_request(self):
        """
        Ensure we get a CREATED on post device location with existing id
        """
        factory = APIRequestFactory()
        request = factory.post(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI, INVALID_DATA_LOCATION, format='json')
        response = device_location(request, id=DEVICE_ID)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_existing_device__when_post_device_location__with_non_existent_device_id__then_return_not_found(self):
        """
        Ensure we get a NOT FOUND when pass a non existent device id on request
        """
        factory = APIRequestFactory()
        request = factory.post(DEVICE_URI + NON_EXISTENT_DEVICE_ID_URI + LOCATION_URI, DATA_LOCATION, format='json')
        response = device_location(request, id=NON_EXISTENT_DEVICE_ID)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_post_device_location__with_existent_device_id__then_new_location_exist(
            self):
        """
        Ensure we insert the new location into the database
        """
        factory = APIRequestFactory()
        request = factory.post(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI, INVALID_DATA_LOCATION, format='json')
        device_location(request, id=DEVICE_ID)
        location = Location.objects.filter(id=1)
        self.assertIsNotNone(self, location)

    """
    PUT devices/:id/ipAddress
    """

    def test_given_existing_device__when_put_device_ip_address__with_invalid_data__then_return_bad_request(self):
        factory = APIRequestFactory()
        request = factory.put(DEVICE_URI + DEVICE_ID_URI + IP_ADDRESS_URI, INVALID_DATA_IP_ADDRESS, format='json')
        response = device_ip_address(request, id=DEVICE_ID)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
