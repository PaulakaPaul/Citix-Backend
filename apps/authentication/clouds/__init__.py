import logging

from apps.authentication.models import User
from requests import HTTPError
from rest_framework import fields
from rest_framework.serializers import Serializer

from apps.authentication.clouds.firebase import FirebaseAuthClient

logger = logging.getLogger(__name__)

auth_cloud_client = FirebaseAuthClient()


def get_auth_cloud_client():
    return auth_cloud_client


class BaseAuthSerializer(Serializer):
    auth_cloud_client_handler = None
    auth_fail_error_class = None

    email = fields.EmailField(required=True)
    password = fields.CharField(required=True)

    def create(self, validated_data):
        assert self.auth_cloud_client_handler is not None

        email = validated_data['email']
        password = validated_data['password']

        try:
            auth_cloud_clientt = get_auth_cloud_client()
            cloud_handler = getattr(auth_cloud_clientt, self.auth_cloud_client_handler)
            user = cloud_handler(email, password)
        except HTTPError as err:
            logger.error(err)
            if self.auth_fail_error_class is None:
                raise err

            raise self.auth_fail_error_class()

        user = self.create_or_get_django_user_from_cloud_user(user)

        # TODO: Return user after it's model it's added.
        return type("User", (), {"email": email, "password": password, "user": user})

    def create_or_get_django_user_from_cloud_user(self, user):
        raise NotImplementedError()




