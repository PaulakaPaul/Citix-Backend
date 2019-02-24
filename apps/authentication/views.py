from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet
import apps.authentication.serializers as serializers
from apps.authentication.models import *


class EmailSignupView(CreateAPIView):
    serializer_class = serializers.EmailSignUpSerializer


class EmailLoginView(CreateAPIView):
    serializer_class = serializers.EmailLoginSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.BaseUserSerializer
    queryset = User.objects.all()


class UserAddressView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserAddressSerializer
    queryset = UserAddress.objects.all()


class UserRatingView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserRatingSerializer
    queryset = UserRating.objects.all()


class UserEventView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserEventSerializer
    queryset = BaseUserEvent.objects.all()
