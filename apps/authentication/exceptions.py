from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class EmailExistsError(APIException):
    message = _('Email already exists.')
    code = 'email_already_exists'
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(self.message, self.code)
