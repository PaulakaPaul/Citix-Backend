import logging

from django.conf import settings
from requests import HTTPError
from rest_framework import fields
from rest_framework.serializers import Serializer
from django.apps import apps

from apps.authentication.clouds.firebase import FirebaseAuthClient
from apps.authentication.models import CloudGeneratedToken

logger = logging.getLogger(__name__)

auth_cloud_client = FirebaseAuthClient()


def get_auth_cloud_client():
    return auth_cloud_client


class BaseAuthSerializer(Serializer):
    auth_cloud_client_handler = None
    auth_fail_error_class = None

    email = fields.EmailField(required=True)
    password = fields.CharField(required=True, write_only=True)

    token = fields.CharField(read_only=True)

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

        cloud_user = user

        user = self.create_or_get_django_user_from_cloud_user(cloud_user)
        self._test_if_valid_model(user)

        token = self.create_and_get_cloud_token(cloud_user, user)
        self._test_if_valid_token(token)

        return {'email': email, 'token': token.key}

    def _test_if_valid_model(self, user):
        user_model = apps.get_model(*settings.AUTH_USER_MODEL.split('.', 1))
        assert isinstance(user, user_model)
        assert user_model is not None

    def _test_if_valid_token(self, token):
        assert isinstance(token, CloudGeneratedToken)
        assert token is not None

    def create_and_get_cloud_token(self, cloud_user, django_user):
        # TODO: Add refresh token login (token expires in 1 hour)
        raise NotImplementedError()

    def create_or_get_django_user_from_cloud_user(self, user):
        raise NotImplementedError()




