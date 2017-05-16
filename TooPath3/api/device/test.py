from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.api.device.serializer import LocationSerializer
from TooPath3.api.device.views import device_location
from TooPath3.api.models import Device

DEVICE_URI = '/devices/'
DEVICE_ID_URI = '1'
LOCATION_URI = '/location'


class DeviceTests(APITestCase):
    def setUp(self):
        Device.objects.create(did=1, name='car', location=Point(40.1234, 2.1234), device_type='ad', device_privacy='pr')

    def test_given_one_device__when_get_device_location__with_existing_device_id__then_return_latitude_and_longitude(
            self):
        """
        Ensure we can get the location from a device
        """
        factory = APIRequestFactory()
        request = factory.get('/devices/1/location')
        response = device_location(request, id=1)
        self.assertEqual(response.data, {'latitude': 40.1234, 'longitude': 2.1234})
