from rest_framework.generics import CreateAPIView

import apps.authentication.serializers as serializers


class EmailSignupView(CreateAPIView):
    serializer_class = serializers.EmailSignUpSerializer


class EmailLoginView(CreateAPIView):
    serializer_class = serializers.EmailLoginSerializer
