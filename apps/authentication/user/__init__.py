from requests import HTTPError
from rest_framework import fields
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.serializers import Serializer
from django.db import models

from apps.authentication.models import *

class BaseUserSerializer(Serializer):
    first_name = fields.CharField(max_length=30, required=True)
    last_name = fields.CharField(max_length=150, required=True)
    phone = fields.CharField(max_length=255)
    email = fields.EmailField(required=True)

    def get_fields(self):
        if self.email or self.first_name or self.last_name is not None:
            try:
                user = super().get_fields()
            except HTTPError as err:
                raise err
        assert user is not None, user

    def update(self, instance, validated_data):
        new_email = validated_data.get('email adress')
        new_first_name = validated_data.get('first name')
        new_last_name = validated_data.get('last name')
        new_phone = validated_data.get('phone number')
        if new_email or new_first_name or new_last_name or new_phone is not None:
            try:
                user = super().update()
            except HTTPError as err:
                raise err
        assert user is not None, user

    def __delete__(self, instance):
        raise NotImplementedError


class BaseUserRatingSerializer(Serializer):
    starRating = models.IntegerField('star rating', blank=True)
    userId = models.OneToOneField('user id', on_delete=True)

    def get_fields(self):
        if self.starRating and self.userId is not None:
            try:
                user_rating = super().get_fields()
            except HTTPError as err:
                raise err
            assert user_rating is not None, user_rating

    def update(self, instance, validated_data):
        new_star_rating = validated_data.get('star rating')
        new_user_id = validated_data.get('user id')

        if new_star_rating and new_user_id is not None:
            try:
                user_rating = super().update()
            except HTTPError as err:
                raise err
            assert user_rating is not None, user_rating

    def create(self, validated_data):
        if self.starRating and self.userId is not None:
            user_rating = UserRating(self.starRating, self.userId)
            super().create()
            assert user_rating is not None, user_rating

    def __delete__(self, instance):
        raise NotImplementedError


class BaseUserAddressSerializer(Serializer):
    country = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    neighbourhood = fields.CharField(max_length=100)
    street = fields.CharField(max_length=50)
    number = fields.CharField(max_length=50)
    userId = models.OneToOneField('user id', on_delete=True)

    def get_fields(self):
        if self.country or self.city or self.neighbourhood \
                or self.street or self.number or self.userId is not None:
            try:
                user_address = super().get_fields()
            except HTTPError as err:
                raise err
            assert user_address is not None, user_address

    def update(self, instance, validated_data):
        new_country = validated_data.get('country name')
        new_city = validated_data.get('city name')
        new_neighbourhood = validated_data.get('neighbourhood')
        new_street = validated_data.get('street adress')
        new_number = validated_data.get('number adress')
        new_user_id = validated_data.get('user id')

        if new_country or new_city or new_neighbourhood or new_street \
                or new_number or new_user_id is not None:
            try:
                user_address = super().update()
            except HTTPError as err:
                raise err
            assert user_address is not None, user_address

    def create(self, validated_data):
        if self.country or self.city or self.neighbourhood \
                or self.street or self.number or self.userId is not None:
            user_address = UserAdress(self.country,
                                      self.city,
                                      self.neighbourhood,
                                      self.street,
                                      self.number,
                                      self.userId)
            super().create()
            assert user_address is not None, user_address

    def __delete__(self, instance):
        raise NotImplementedError

# Abstract Models


class AbstractUserAddress:

    country = models.CharField('country name', max_length=50, blank=True)
    city = models.CharField('city name', max_length=50, blank=True)
    neighbourhood = models.CharField('neightbourhood name', max_length=100, blank=True)
    street = models.CharField('street address', blank=True, max_length=50)
    number = models.CharField('number address', blank=True, max_length=50)
    userId = models.OneToOneField('user id',on_delete=True)

    COUNTRY_FIELD = 'country'
    CITY_FIELD = 'city'
    NEIGHBOURHOOD_FIELD = 'neighbourhood'
    STREET_FIELD = 'street'
    NUMBER_FIELD = 'number'
    USERID_FIELD = 'userId'
    REQUIRED_FIELDS = ['country', 'city', 'neighbourhood', 'street']

    class Meta:
        verbose_name = 'userAdress'
        verbose_name_plural = 'usersAdress'
        abstract = True

    def clean(self):
        raise NotImplementedError

    def get_full_address(self):
        full_name = '%s %s %s %s ' % (self.country, self.city, self.neighbourhood, self.street)
        return full_name.strip()

    def get_city(self):
        return self.city

    def get_id(self):
        return self.userId


class AbstractUserRating:

    starRating = models.IntegerField('star rating', blank=True)
    userId = models.OneToOneField('user id',on_delete=True)

    STAR_RATING = 'star rating'
    USERID_FIELD = 'userId'
    REQUIRED_FIELDS = ['star rating', 'userId']

    class Meta:
        verbose_name = 'userRating'
        verbose_name_plural = 'usersRating'
        abstract = True

    def clean(self):
        raise NotImplementedError

    def get_rating(self):
        return self.starRating


