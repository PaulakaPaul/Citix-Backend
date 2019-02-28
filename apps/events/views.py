from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.events import serializers
from apps.events.models import Event


class EventViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
