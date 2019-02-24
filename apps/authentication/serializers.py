from rest_framework import serializers
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


class BaseUserSerializer(serializers.Serializer):
    first_name = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, required=True, allow_blank=False)
    last_name = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, required=True, allow_blank=False)
    phone = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR)
    email = fields.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.phone = validated_data.get('phone')
        instance.email = validated_data.get('email')
        instance.save()
        user = instance.user
        user.save()


class UserAddressSerializer(serializers.Serializer):
    country = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    city = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    neighbourhood = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    street = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR)
    number = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR)

    class Meta:
        model = UserAddress
        fields = ('country', 'city', 'neighbourhood', 'street', 'number', 'user')

    user = BaseUserSerializer(required=True)

    def create(self, validated_data):
        user = BaseUserSerializer(self.user, first_name=validated_data.pop('first_name'),
                                  last_name=validated_data.pop('last_name'),
                                  phone=validated_data.pop('phone'),
                                  email=validated_data.pop('email'))
        user.is_valid(raise_exception=True)

        return UserAddress.objects.update_or_create(country=validated_data.pop('country'),
                                                    city=validated_data.pop('city'),
                                                    neighbourhood=validated_data.pop('neighbourhood'),
                                                    street=validated_data.pop('street'),
                                                    number=validated_data.pop('number'),
                                                    user=user)

    def update(self, instance, validated_data):
        instance.country = validated_data.get('country')
        instance.city = validated_data.get('city')
        instance.neighbourhood = validated_data.get('neighbourhood')
        instance.street = validated_data.get('street')
        instance.number = validated_data.get('number')
        instance.user = validated_data.get('user')
        instance.save()
        user_address = instance
        user_address.save()


class UserRatingSerializer(serializers.Serializer):
    star_rating = fields.IntegerField()
    user = BaseUserSerializer(required=True)

    class Meta:
        model = UserRating
        fields = ('star_rating', 'user')

    def create(self, validated_data):
        user = BaseUserSerializer(self.user, first_name=validated_data.pop('first_name'),
                                  last_name=validated_data.pop('last_name'),
                                  phone=validated_data.pop('phone'),
                                  email=validated_data.pop('email'))
        user.is_valid(raise_exception=True)

        return UserAddress.objects.update_or_create(star_rating=validated_data.pop('star_rating'),
                                                    user=user)

    def update(self, instance, validated_data):
        instance.star_rating = validated_data.get('star_rating')
        instance.user_id = validated_data.get('user')
        instance.save()
        user_rating = instance.user
        user_rating.save()


class _LocationSerializer(serializers.Serializer):
    x = fields.IntegerField()
    y = fields.IntegerField()

    def create(self, validated_data):
        return Location.objects.update_or_create(**validated_data)


class _EventSerializer(serializers.Serializer):
    name = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    description = fields.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR, allow_blank=False)
    photo_urls = fields.ListField(serializers.CharField(max_length=_constants.QUERY_STRINGS_LENGTH_ADDR*100),
                                  max_length=10)
    location = _LocationSerializer(required=True)

    def create(self, validated_data):
        location = _LocationSerializer(self.location, x=validated_data.pop('x'), y=validated_data.pop("y"))
        location.is_valid(raise_exception=True)

        return Event.objects.update_or_create(name=validated_data.pop('name'),
                                              description=validated_data.pop('description'),
                                              photo_urls=validated_data.pop('photo_urls'),
                                              location=location)


class UserEventSerializer(serializers.Serializer):
    event = _EventSerializer(required=True)
    user = BaseUserSerializer(required=True)

    def create(self, validated_data):
        event = _EventSerializer.create(self.event, **validated_data)
        event.is_valid(raise_exception=True)
        user = BaseUserSerializer.create(self.user, **validated_data)

        return BaseUserEvent.objects.update_or_create(event=event, user=user)
