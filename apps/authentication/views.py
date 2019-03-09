from rest_framework import mixins
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import GenericViewSet
import apps.authentication.serializers as serializers
from apps.authentication.models import *
from apps.common.base_views import BaseAddPhotoView


class EmailSignupView(CreateAPIView):
    serializer_class = serializers.EmailSignUpSerializer
    permission_classes = ()


class EmailLoginView(CreateAPIView):
    serializer_class = serializers.EmailLoginSerializer
    permission_classes = ()


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class CurrentUserView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserAddPhotoView(BaseAddPhotoView):
    model = User
