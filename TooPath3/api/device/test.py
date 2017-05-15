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
        Device.objects.create(name='my_car', location=Point(40.1234, 2.1234), device_type='ad', device_privacy='pr')
        print("device 1 inserted")

    def test_get_location(self):
        """
        Ensure we can get the location from a device
        """
        factory = APIRequestFactory()
        request = factory.get('/devices/1/location')
        response = device_location(request, id=1)
        self.assertEqual(response.data, {'latitude': 40.1234, 'longitude': 2.1234})

    def test_put_location(self):
        """
        Ensure we can get the location from a device
        """
        factory = APIRequestFactory()
        data = {'latitude': 45.1234, 'longitude': 4.1234, 'did': 1}
        request = factory.post(DEVICE_URI + DEVICE_ID_URI + LOCATION_URI, data, format='json')
        response = device_location(request, id=1)
        # serializer = LocationSerializer(data=data)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(serializer.data, {'latitude': 45.1234, 'longitude': 4.1234, 'did': 1})
