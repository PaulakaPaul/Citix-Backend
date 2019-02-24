from rest_framework import serializers
from apps.authentication.user import BaseUserSerializer
from apps.authentication.clouds import BaseAuthSerializer
from apps.authentication.models import *
from rest_framework import fields
from apps.authentication.user import _constants

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

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserAddressSerializer(serializers.Serializer):
    country = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    city = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    neighbourhood = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    street = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR)
    number = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR)

    class Meta:
        model = UserAddress
        fields = ('country', 'city', 'neighbourhood', 'street', 'number', 'user_id')

    user_id = UserSerializer(required=True)

    def create(self, validated_data):
        user = UserSerializer.create(UserSerializer(), validated_data=validated_data.pop('user'))
        return UserAddress.objects.update_or_create(country=validated_data.pop('country'),
                                                    city=validated_data.pop('city'),
                                                    neighbourhood=validated_data.pop('neighbourhood'),
                                                    street=validated_data.pop('street'),
                                                    number=validated_data.pop('number'),
                                                    user_id=user)

    def update(self, instance, validated_data):
        instance.country = validated_data.get('country')
        instance.city = validated_data.get('city')
        instance.neighbourhood = validated_data.get('neighbourhood')
        instance.street = validated_data.get('street')
        instance.number = validated_data.get('number')
        instance.user_id = validated_data.get('user_id')
        instance.save()
        user_address = instance.user
        user_address.save()


class UserRatingSerializer(serializers.Serializer):
    star_rating = fields.IntegerField()

    user_id = UserSerializer(required=True)

    class Meta:
        model = UserRating
        fields = ('star_rating', 'user_id')

    def create(self, validated_data):
        user = UserSerializer.create(UserSerializer(), validated_data=validated_data.pop('user'))
        return UserAddress.objects.update_or_create(star_rating=validated_data.pop('star_rating'),
                                                    user_id=user)

    def update(self, instance, validated_data):
        instance.star_rating = validated_data.get('star_rating')
        instance.user_id = validated_data.get('user_id')
        instance.save()
        user_rating = instance.user
        user_rating.save()
