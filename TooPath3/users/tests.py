import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from TooPath3.models import CustomUser
from TooPath3.users.views import *

# DATA CONSTANTS
VALID_DATA_USER = {
    "username": "test",
    "email": "test@test.com",
    "password": "password"
}
INVALID_DATA_USER = {
    "username": "test"
}
VALID_DATA_LOGIN = {
    "username": "test",
    "password": "test"
}
INVALID_DATA_LOGIN = {
    "user": "test",
    "pssword": "test"
}
DATA_LOGIN_NO_PASSWORD = {
    "username": "test"
}
DATA_LOGIN_NO_USERNAME = {
    "password": "test"
}

UserModel = get_user_model()


class UserTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    """
    GET  /users
    """
    """
    POST /users
    """

    def test_given_non_existing_users__when_post_users__with_username_email_and_password__then_return_created(self):
        response = self.client.post('/users/', VALID_DATA_USER, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_given_non_existing_users__when_post_users__with_username_email_and_password__then_user_is_created(self):
        self.client.post('/users/', VALID_DATA_USER, format='json')
        user = CustomUser.objects.get(username='test')
        self.assertEqual(user.email, 'test@test.com')

    def test_given_non_existing_users__when_post_users__with_invalid_username_email_or_password__then_return_bad_request(
            self):
        response = self.client.post('/users/', INVALID_DATA_USER, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_non_existing_users__when_post_users__with_username_email_and_password__then_return_token(self):
        response = self.client.post('/users/', VALID_DATA_USER, format='json')
        self.assertIsNotNone(response.data['token'])


class TokenTest(APITestCase):
    class PayloadObject:
        def __init__(self, username, pk):
            self.username = username
            self.pk = pk

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username="test", email='test@test.com', password=make_password('test'))

    """
    POST /login
    """

    def test_given_existing_user__when_post_login__with_valid_username_and_password__then_return_ok(self):
        response = self.client.post('/login/', VALID_DATA_LOGIN, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_given_existing_user__when_post_login__with_valid_username_and_password__then_return_token(self):
        response = self.client.post('/login/', VALID_DATA_LOGIN, format='json')
        self.assertIsNotNone(response.data['token'])

    def test_given_existing_user__when_post_login__with_invalid_username_or_password__then_return_bad_request(self):
        response = self.client.post('/login/', INVALID_DATA_LOGIN, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_given_existing_user__when_post_login__with_no_password__then_return_password_needed_error(self):
        response = self.client.post('/login/', DATA_LOGIN_NO_PASSWORD, format='json')
        self.assertEqual(response.data['password'], ['This field is required.'])

    def test_given_existing_user__when_post_login__with_no_username__then_return_username_needed_error(self):
        response = self.client.post('/login/', DATA_LOGIN_NO_USERNAME, format='json')
        self.assertEqual(response.data['username'], ['This field is required.'])

    def test_given_existing_user__when_post_verify_token__with_generated_token__then_return_ok_status(self):
        user_jwt_secret = str(self.user.jwt_secret)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        payload_object = TokenTest.PayloadObject(self.user.username, self.user.pk)
        payload = jwt_payload_handler(payload_object)
        token = jwt.encode(
            payload,
            user_jwt_secret,
            api_settings.JWT_ALGORITHM
        ).decode('utf-8')
        response = self.client.post('/api-token-verify/', {"token": token}, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
