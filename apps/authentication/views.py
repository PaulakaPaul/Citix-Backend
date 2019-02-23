from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet

import apps.authentication.serializers as serializers
from apps.authentication.models import User


class EmailSignupView(CreateAPIView):
    serializer_class = serializers.EmailSignUpSerializer


class EmailLoginView(CreateAPIView):
    serializer_class = serializers.EmailLoginSerializer


class UserView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class UserAdressView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserAddressSerializer
    queryset = User.objects.all()


class UserRatingView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserRatingSerializer
    queryset = User.objects.all()
