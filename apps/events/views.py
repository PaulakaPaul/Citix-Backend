from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.events import serializers
from apps.events.models import Event, EventUserReaction


class EventViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()


class EventUserReactionViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = serializers.EventUserReactionSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        event_id = request.data.get('event_id')

        try:
            event_user_reaction = EventUserReaction.objects.get(user_id=user_id, event_id=event_id)
            event_user_reaction.delete()
        except EventUserReaction.DoesNotExist:
            pass

        return super().create(request, *args, **kwargs)
