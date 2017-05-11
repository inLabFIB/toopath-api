from TooPathAPI.models import Device
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.api.device import device_location


class DeviceTests(APITestCase):
    def setUp(self):
        Device.objects.create(name='my_car', location=Point(40.1234, 2.1234), device_type='ad', device_privacy='pr')

    def test_get_location(self):
        """
        Ensure we can get the location from a device
        """
        factory = APIRequestFactory()
        request = factory.get('/devices/1/location')
        response = device_location(request, id=1)
        response.render()
        self.assertEqual(response.content, '{"latitude":40.1234,"longitude":2.1234}')
