from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.authentication.clouds import BaseAuthSerializer
from apps.authentication.models import *
import apps.authentication.models as models
import apps.authentication.exceptions as exceptions


class EmailSignUpSerializer(BaseAuthSerializer):
    auth_cloud_client_handler = 'create_user_with_email_and_password'
    auth_fail_error_class = exceptions.EmailExistsError

    def create_or_get_django_user_from_cloud_user(self, user):
        new_django_user = User.objects.create(email=user['email'])

        return new_django_user

    def create_and_get_cloud_token(self, cloud_user, django_user):
        token = cloud_user['idToken']
        refresh_token = cloud_user['refreshToken']

        return CloudGeneratedToken.objects.create(key=token, refresh_key=refresh_token, user=django_user)


class EmailLoginSerializer(BaseAuthSerializer):
    auth_cloud_client_handler = 'sign_in_with_email_and_password'
    auth_fail_error_class = exceptions.WrongEmailOrPasswordError

    def create_or_get_django_user_from_cloud_user(self, user):
        persisted_django_user = User.objects.get(email=user['email'])

        return persisted_django_user

    def create_and_get_cloud_token(self, cloud_user, django_user):
        token = cloud_user['idToken']
        refresh_token = cloud_user['refreshToken']

        try:
            # Because the key is primary key the token cannot be updated.
            cloud_token = CloudGeneratedToken.objects.get(user=django_user)
            cloud_token.delete()
        except CloudGeneratedToken.DoesNotExist:
            pass

        return CloudGeneratedToken.objects.create(key=token, refresh_key=refresh_token, user=django_user)


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserAddress
        fields = ('country', 'city', 'neighbourhood', 'street', 'number')


class UserRatingSerializer(serializers.ModelSerializer):
    star_rating = serializers.FloatField(required=True)

    class Meta:
        model = models.UserRating
        fields = ('star_rating', )


class UserSerializer(serializers.ModelSerializer):
    addresses = UserAddressSerializer(many=True, required=False)
    rating = UserRatingSerializer(many=False, required=False)

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'addresses', 'rating', 'photo_urls')
        read_only_fields = ('id', 'email', 'photo_urls')

    def validate_rating(self, value):
        if value is not None and len(value) == 0:
            raise serializers.ValidationError(_('Empty rating object not supported.'))

        if value:
            star_rating = value.get('star_rating', None)
            if star_rating and star_rating > 5.0:
                raise serializers.ValidationError(_('Star rating max value is 5.0.'))

        return value

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', None)
        star_rating_data = validated_data.pop('star_rating', None)

        user = User.objects.create(**validated_data)

        with transaction.atomic():
            user.save()

            if addresses_data:
                for address_data in addresses_data:
                    self._create_address(user, address_data)

            if star_rating_data:
                self._create_star_rating(user, star_rating_data)

        return user

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', None)
        star_rating_data = validated_data.pop('rating', None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            if addresses_data:
                for address_data in addresses_data:
                    self._create_address(instance, address_data)

            if star_rating_data:
                instance.rating.delete()
                self._create_star_rating(instance, star_rating_data)

        return instance

    def _create_address(self, user, address_data):
        address_serializer = UserAddressSerializer(data=address_data)
        if address_serializer.is_valid(raise_exception=True):
            address_serializer.save(user=user)

    def _create_star_rating(self, user, star_rating_data):
        star_rating_serializer = UserRatingSerializer(data=star_rating_data)
        if star_rating_serializer.is_valid(raise_exception=True):
            star_rating_serializer.save(user=user)
