from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory

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

UserModel = get_user_model()


class UserTest(APITestCase):
    """
    GET  /users
    """
    """
    POST /users
    """

    def test_given_non_existing_users_when_post_users__with_username_email_and_password__then_return_created(self):
        factory = APIRequestFactory()
        request = factory.post('/users', VALID_DATA_USER, format='json')
        response = new_user(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_given_non_existing_users_when_post_users__with_username_email_and_password__then_user_is_created(self):
        factory = APIRequestFactory()
        request = factory.post('/users', VALID_DATA_USER, format='json')
        new_user(request)
        user = UserModel.objects.get(username='test')
        self.assertEqual(user.email, 'test@test.com')

    def test_given_non_existing_users_when_post_users__with_invalid_username_email_or_password__then_return_bad_request(
            self):
        factory = APIRequestFactory()
        request = factory.post('/users', INVALID_DATA_USER, format='json')
        response = new_user(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
