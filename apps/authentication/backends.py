from rest_framework.authentication import TokenAuthentication

from apps.authentication.models import CloudGeneratedToken


class CloudTokenAuthentication(TokenAuthentication):
    model = CloudGeneratedToken
