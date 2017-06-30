from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.location.views import *
from TooPath3.models import Device

# DATA constants
DATA_LOCATION = {
    'latitude': 40.1234,
    'longitude': 2.1234
}


class ActualLocationTests(APITestCase):
    def setUp(self):
        Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr')

    """
    POST /devices/:id/location
    """

    def test_given_existing_device__when_post_device_location_with_existing_device_id__then_return_created(self):
        factory = APIRequestFactory()
        request = factory.post('/devices/1/location', DATA_LOCATION, format='json')
        response = device_location(request, id=1)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
