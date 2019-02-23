# from allauth.account.adapter import get_adapter
# from allauth.account.models import EmailAddress
# from allauth.account.utils import setup_user_email


from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext
from rest_auth.registration.serializers import RegisterSerializer as RestRegisterSerializer
from rest_auth.serializers import LoginSerializer as RestLoginSerializer
from rest_auth.serializers import PasswordChangeSerializer as RestPasswordChangeSerializer
from rest_auth.serializers import PasswordResetConfirmSerializer as RestPasswordResetConfirmSerializer
from rest_auth.serializers import PasswordResetSerializer as RestPasswordResetSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

