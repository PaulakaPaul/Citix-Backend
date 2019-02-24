from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet
import apps.authentication.serializers as serializers
from apps.authentication.models import User


class EmailSignupView(CreateAPIView):
    serializer_class = serializers.EmailSignUpSerializer


class EmailLoginView(CreateAPIView):
    serializer_class = serializers.EmailLoginSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    search_fields = ('first_name', 'last_name', 'phone', 'email')

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserAddressView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserAddressSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserRatingView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserRatingSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
