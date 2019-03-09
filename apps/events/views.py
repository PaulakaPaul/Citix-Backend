from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.common.base_views import BaseAddPhotoView
from apps.events import serializers
from apps.events.models import Event, EventUserReaction


class EventViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()


class EventUserReactionViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = serializers.EventUserReactionSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        event_id = request.data.get('event_id')

        interested = request.data.get('interested', False)
        going = request.data.get('going', False)

        try:
            event_user_reaction = EventUserReaction.objects.get(user_id=user_id, event_id=event_id)
            event_user_reaction.delete()
        except EventUserReaction.DoesNotExist:
            pass

        if interested is False and going is False:
            delete_response_data = {
                "message": "Reaction deleted."
            }

            return Response(delete_response_data, status=status.HTTP_201_CREATED)

        return super().create(request, *args, **kwargs)


class EventAddPhotoView(BaseAddPhotoView):
    model = Event
