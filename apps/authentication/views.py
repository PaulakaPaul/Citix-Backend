from rest_framework.generics import CreateAPIView

from apps.authentication.serializers import EmailSignUpSerializer


class EmailSignupView(CreateAPIView):
    serializer_class = EmailSignUpSerializer
