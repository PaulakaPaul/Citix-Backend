from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class FieldError(ValidationError):
    message = ValidationError.default_detail
    code = ValidationError.default_code

    def __init__(self, field=None):
        if field is None:
            detail = [self.message]
        else:
            detail = {field: [self.message]}

        super().__init__(detail, code=self.code)


class EmailExistsError(FieldError):
    message = _('Email already exists.')
    code = 'email_already_exists'

    def __init__(self):
        super().__init__('email')


class WrongEmailOrPasswordError(FieldError):
    message = _('Wrong email or password')
    code = 'wrong_email_or_password'

    def __init__(self):
        super().__init__('credentials')
