from rest_framework.status import *
from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.devices.views import device
from TooPath3.models import Device


class DevicesTest(APITestCase):
    def setUp(self):
        Device.objects.create(did=1, name='car', ip_address='0.0.0.0', device_type='ad', device_privacy='pr')

    """ 
    GET /devices/:id/actualLocation 
    """

    def test_given_existing_device__when_get_device_with_existing_device_id__then_return_ok(self):
        factory = APIRequestFactory()
        request = factory.get('/devices/1', format='json')
        response = device(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_get_device_with_non_existing_device_id__then_return_not_found(self):
        factory = APIRequestFactory()
        request = factory.get('/devices/1', format='json')
        response = device(request, id=10)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
