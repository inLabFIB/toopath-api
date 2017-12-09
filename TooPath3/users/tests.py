import jwt
from rest_framework.test import APITestCase, APIClient

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.users.views import *
from TooPath3.utils import create_user_with_email, generate_token_for_testing, get_latest_id_inserted


class GetUserCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('user@gmail.com')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_user_not_exists(self):
        response = self.client.get(path='/users/100/')
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_is_not_self(self):
        new_user = create_user_with_email('user2@gmail.com')
        response = self.client.get(path='/users/' + str(new_user.pk) + '/')
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(path='/users/1/')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_200_status_when_get_user_is_done(self):
        response = self.client.get(path='/users/' + str(self.user.pk) + '/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_with_user_info_status_when_get_user_is_done(self):
        response = self.client.get(path='/users/' + str(self.user.pk) + '/')
        self.assertEqual(PublicCustomUserSerializer(instance=self.user).data, response.data)


class PostUserCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_return_201_status_when_post_user_is_done(self):
        json_body = {'username': 'test', 'email': 'test@gmail.com', 'password': 'test_password'}
        response = self.client.post(path='/users/', data=json_body, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_instance_is_created_when_post_user_is_done(self):
        json_body = {'username': 'test', 'email': 'test@gmail.com', 'password': 'test_password'}
        self.client.post(path='/users/', data=json_body, format='json')
        user_created = CustomUser.objects.get(pk=get_latest_id_inserted(model_class=CustomUser))
        self.assertIsNotNone(user_created)

    def test_return_json_response_status_when_post_user_is_done(self):
        json_body = {'username': 'test', 'email': 'test@gmail.com', 'password': 'test_password'}
        response = self.client.post(path='/users/', data=json_body, format='json')
        user_created = CustomUser.objects.get(pk=get_latest_id_inserted(model_class=CustomUser))
        self.assertEqual(response.data, PublicCustomUserSerializer(instance=user_created).data)

    def test_return_400_status_when_json_body_is_invalid(self):
        json_body_invalid = {'user_name': 'test', 'email': 'test@gmail.com', 'password': 'test_password'}
        response = self.client.post(path='/users/', data=json_body_invalid, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

class PatchUserCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('test@gmail.com')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_user_not_exists(self):
        response = self.client.patch(path='/users/100/', data={})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_is_not_self(self):
        new_user = create_user_with_email('user2@gmail.com')
        response = self.client.patch(path='/users/' + str(new_user.pk) + '/', data={})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.patch(path='/users/1/', data={})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        json_data = {'name': 'test', 'last_name': 'refactor'}
        response = self.client.patch(path='/users/' + str(self.user.pk) + '/', data=json_data)
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_return_error_message_status_when_try_to_modify_instance_representation(self):
        json_data = {'email': 'newtest@gmail.com'}
        response = self.client.patch(path='/users/' + str(self.user.pk) + '/', data=json_data)
        expected_error = {'non_field_errors': [DEFAULT_ERROR_MESSAGES['invalid_patch']]}
        self.assertEqual(expected_error, response.data)

    def test_return_200_status_when_user_is_patched(self):
        json_data = {'first_name': 'test', 'last_name': 'refactor'}
        response = self.client.patch(path='/users/' + str(self.user.pk) + '/', data=json_data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_with_user_info_status_when_get_user_is_done(self):
        json_data = {'first_name': 'test', 'last_name': 'refactor'}
        response = self.client.patch(path='/users/' + str(self.user.pk) + '/', data=json_data)
        user_updated = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(PublicCustomUserSerializer(instance=user_updated).data, response.data)


class PutUserCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_email('test@gmail.com')
        self.token = generate_token_for_testing(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_return_404_status_when_user_not_exists(self):
        response = self.client.put(path='/users/100/', data={})
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_return_403_status_when_user_is_not_self(self):
        new_user = create_user_with_email('user2@gmail.com')
        response = self.client.put(path='/users/' + str(new_user.pk) + '/', data={})
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_return_401_status_when_user_is_not_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.put(path='/users/1/', data={})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_return_400_status_when_json_body_is_invalid(self):
        json_data = {'name': 'test', 'last_name': 'refactor'}
        response = self.client.put(path='/users/' + str(self.user.pk) + '/', data=json_data)
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_return_200_status_when_user_is_patched(self):
        json_data = {'email': 'test@gmail.com', 'username': 'testing', 'password': 'text', 'first_name': 'test',
                     'last_name': 'refactor'}
        response = self.client.put(path='/users/' + str(self.user.pk) + '/', data=json_data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_return_json_with_user_info_status_when_get_user_is_done(self):
        json_data = {'email': 'test@gmail.com', 'username': 'testing', 'password': 'text', 'first_name': 'test',
                     'last_name': 'refactor'}
        response = self.client.put(path='/users/' + str(self.user.pk) + '/', data=json_data)
        user_updated = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(PublicCustomUserSerializer(instance=user_updated).data, response.data)

"""
class LoginTest(APITestCase):

    class PayloadObject:
        def __init__(self, username, pk):
            self.username = username
            self.pk = pk

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username="test", email='test@test.com', password=make_password('test'))

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
        payload_object = LoginTest.PayloadObject(self.user.username, self.user.pk)
        payload = jwt_payload_handler(payload_object)
        token = jwt.encode(
            payload,
            user_jwt_secret,
            api_settings.JWT_ALGORITHM
        ).decode('utf-8')
        response = self.client.post('/api-token-verify/', {"token": token}, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)"""