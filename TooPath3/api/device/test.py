from django.contrib.gis.geos import Point
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.api.device.views import device_location
from TooPath3.api.models import Device

# URI constants
DEVICE_URI = '/devices/'
DEVICE_ID_URI = '1'
LOCATION_URI = '/location'

# DATA constants
DATA_GET_AND_POST = {'latitude': 40.1234, 'longitude': 2.1234}
DATA_GET_AND_POST_BAD_FORMAT = {'lat': 40.1234, 'long': 2.1234}
DEVICE_ID = 1


class DeviceTests(APITestCase):
    def setUp(self):
        Device.objects.create(did=1, name='car', location=Point(40.1234, 2.1234), device_type='ad', device_privacy='pr')

    def test_given_existing_device__when_get_device_location__with_existing_device_id__then_return_latitude_and_longitude(
            self):
        """
        Ensure we can get the location from a device
        """
        factory = APIRequestFactory()
        request = factory.get(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI)
        response = device_location(request, id=DEVICE_ID)
        self.assertEqual(response.data, DATA_GET_AND_POST)

    def test_given_existing_device__when_post_device_location__with_bad_data_format__then_return_bad_request(self):
        """
        Ensure we get a BAD REQUEST when pass a bad format data on request
        """
        factory = APIRequestFactory()
        request = factory.post(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI, DATA_GET_AND_POST_BAD_FORMAT,
                               content_type='application/json')
        response = device_location(request, id=DEVICE_ID)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
