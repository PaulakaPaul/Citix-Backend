from rest_framework import serializers
from apps.authentication.clouds import BaseAuthSerializer
from apps.authentication.models import User, CloudGeneratedToken
import apps.authentication.exceptions as exceptions


class EmailSignUpSerializer(BaseAuthSerializer):
    auth_cloud_client_handler = 'create_user_with_email_and_password'
    auth_fail_error_class = exceptions.EmailExistsError

    def create_or_get_django_user_from_cloud_user(self, user):
        new_django_user = User.objects.create(email=user['email'])

        return new_django_user

    def get_and_persist_cloud_token(self, cloud_user, django_user):
        token = cloud_user['idToken']
        refresh_token = cloud_user['refreshToken']

        return CloudGeneratedToken.objects.create(key=token, refresh_key=refresh_token, user=django_user)


class EmailLoginSerializer(BaseAuthSerializer):
    auth_cloud_client_handler = 'sign_in_with_email_and_password'
    auth_fail_error_class = exceptions.WrongEmailOrPasswordError

    def create_or_get_django_user_from_cloud_user(self, user):
        persisted_django_user = User.objects.get(email=user['email'])

        return persisted_django_user

    def get_and_persist_cloud_token(self, cloud_user, django_user):
        token = cloud_user['idToken']
        refresh_token = cloud_user['refreshToken']

        try:
            # Because the key is primary key the token cannot be updated.
            cloud_token = CloudGeneratedToken.objects.get(user=django_user)
            cloud_token.delete()
        except CloudGeneratedToken.DoesNotExist:
            pass

        return CloudGeneratedToken.objects.create(key=token, refresh_key=refresh_token, user=django_user)


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    def save(self, validated_data):
        return User(self.first_name, self.last_name, self.email, self.phone).save()

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.first_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        return User(instance.first_name, instance.last_name, instance.email, instance.phone).save()

    def get(self):
        super().get_fields()

    def delete(self):
        super().delete(self)
