from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.location.views import *
from TooPath3.models import Device

# DATA constants
DATA_LOCATION = {
    'latitude': 40.1234,
    'longitude': 2.1234
}
INVALID_DATA_LOCATION = {
    'lat': 40.1234,
    'lon': 2.1234
}


class ActualLocationTests(APITestCase):
    def setUp(self):
        Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr')

    """
    POST /devices/:id/actualLocation
    """

    def test_given_existing_device__when_put_device_actual_location_with_existing_device_id__then_return_created(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', DATA_LOCATION, format='json')
        response = device_actual_location(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_put_device_actual_location_with_invalid_data__then_return_bad_request(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1/actualLocation', INVALID_DATA_LOCATION, format='json')
        response = device_actual_location(request, id=1)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)