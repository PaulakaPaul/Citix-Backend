import logging

from requests import HTTPError
from rest_framework import fields
from rest_framework.serializers import Serializer

from apps.authentication.clouds import get_auth_cloud_client
from apps.authentication.exceptions import EmailExistsError

logger = logging.getLogger(__name__)


class EmailSignUpSerializer(Serializer):
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        try:
            auth_cloud_client = get_auth_cloud_client()
            auth_cloud_client.create_user_with_email_and_password(email, password)
        except HTTPError as err:
            logger.error(err)
            raise EmailExistsError()
