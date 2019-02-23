from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


class UserManager(DefaultUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    phone = models.IntegerField(_('phone number'), blank=True)

    EMAIL_FIELD = 'email'
    FIRST_NAME_FIELD = 'firstName'
    LAST_NAME_FIELD = 'lastName'
    PHONE_FIELD = 'phone'

    backend = ''

    class Meta:
        db_table = 'users'

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        super().__init__(self, first_name, last_name, email, phone)

    def __str__(self):
        if self.first_name and self.last_name is None:
            raise ValidationError('First_name or last_name of the user is None', code='inconsistent')
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.first_name is None or self.last_name is None or self.email is None:
            raise ValidationError('User needs first name, last name or email.', code='inconsistent')

        super().save(*args, **kwargs)


