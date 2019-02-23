from rest_framework import serializers
from apps.authentication.user import BaseUserSerializer, BaseUserRatingSerializer, BaseUserAddressSerializer
from apps.authentication.clouds import BaseAuthSerializer
from apps.authentication.models import User
import apps.authentication.exceptions as exceptions


class EmailSignUpSerializer(BaseAuthSerializer):
    auth_cloud_client_handler = 'create_user_with_email_and_password'
    auth_fail_error_class = exceptions.EmailExistsError

    def create_or_get_django_user_from_cloud_user(self, user):
        # TODO: Create django user.
        return user


class EmailLoginSerializer(BaseAuthSerializer):
    auth_cloud_client_handler = 'sign_in_with_email_and_password'
    auth_fail_error_class = exceptions.WrongEmailOrPasswordError

    def create_or_get_django_user_from_cloud_user(self, user):
        # TODO: Get django user.
        return user


class UserSerializer(BaseUserSerializer):

    def get(self):
        super().get_fields()

    def save(self, **kwargs):
        super().update()


class UserAddressSerializer(BaseUserAddressSerializer):

    def get(self):
        super().get_fields()

    def post(self):
        super().create()

    def save(self, **kwargs):
        super().update()


class UserRatingSerializer(BaseUserRatingSerializer):

    def get(self):
        super().get_fields()

    def post(self):
        super().create()

    def save(self, **kwargs):
        super().update()
