from rest_framework_jwt.settings import api_settings

from TooPath3.models import CustomUser


def get_jwt_secret(user):
    custom_user = CustomUser.objects.get(pk=user.pk)
    return custom_user.jwt_secret


def generate_token_for_testing(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)
