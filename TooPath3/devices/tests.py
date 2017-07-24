from rest_framework.status import *
from rest_framework.test import APITestCase, APIRequestFactory

from TooPath3.devices.views import device_detail
from TooPath3.models import Device

# DATA CONSTANTS
VALID_DATA_DEVICE = {
    "ip_address": "127.0.0.1",
    "port_number": 8000
}
INVALID_DATA_DEVICE = {
    "ip": "127.0.0.1"
}


class DevicesTest(APITestCase):
    def setUp(self):
        Device.objects.create(did=1, name='car', ip_address='0.0.0.0', port_number=8080, device_type='ad', device_privacy='pr')

    """ 
    GET /devices/:id
    """

    def test_given_existing_device__when_get_device_with_existing_device_id__then_return_ok(self):
        factory = APIRequestFactory()
        request = factory.get('/devices/1', format='json')
        response = device_detail(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_get_device_with_non_existing_device_id__then_return_not_found(self):
        factory = APIRequestFactory()
        request = factory.get('/devices/1', format='json')
        response = device_detail(request, id=10)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    """ 
    PUT /devices/:id
    """

    def test_given_existing_device__when_put_device_with_existing_device_id_and_valid_data__then_return_ok(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1', VALID_DATA_DEVICE, format='json')
        response = device_detail(request, id=1)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_device__when_put_device_with_non_existing_device_id_and_valid_data__then_return_ok(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1', VALID_DATA_DEVICE, format='json')
        response = device_detail(request, id=10)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_given_existing_device__when_put_device_with_existing_device_id_and_invalid_data__then_return_ok(self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1', INVALID_DATA_DEVICE, format='json')
        response = device_detail(request, id=1)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_existing_device__when_put_device_with_existing_device_id_and_valid_data__then_return_ip_address(
            self):
        factory = APIRequestFactory()
        request = factory.put('/devices/1', VALID_DATA_DEVICE, format='json')
        device_detail(request, id=1)
        device = Device.objects.get(pk=1)
        self.assertEqual(device.ip_address, '127.0.0.1')
