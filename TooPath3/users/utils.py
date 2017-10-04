from TooPath3.models import CustomUser


def get_jwt_secret(user):
    custom_user = CustomUser.objects.get(pk=user.pk)
    return custom_user.jwt_secret
