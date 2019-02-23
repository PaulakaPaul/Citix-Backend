from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# Create your models here.


class UserManager(DefaultUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    phone = models.IntegerField('phone number', blank=True)

    PHONE_FIELD = 'phone'

    backend = ''

    class Meta:
        db_table = 'users'

    def __init__(self, first_name, last_name, email, phone):
        super().first_name = first_name
        super().last_name = last_name
        super().email = email
        self.phone = phone
        super().__init__(self, first_name, last_name, email, phone)

    def __str__(self):
        return super().get_full_name(self)

    def save(self, *args, **kwargs):
        get_user_model().objects.create_user(self, 'test', self.email, 'test',
                                             self.first_name, self.last_name,
                                             self.phone)

