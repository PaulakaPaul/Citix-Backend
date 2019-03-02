from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.authentication.serializers import UserSerializer, User
from apps.events import models
from apps.events.models import Event


class EventUserReactionSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(source='event', write_only=True, queryset=Event.objects.all())

    user_id = serializers.PrimaryKeyRelatedField(source='user', write_only=True, queryset=User.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.EventUserReaction
        fields = ('user_id', 'user', 'interested', 'going', 'event_id')

    def validate(self, attrs):
        interested = attrs.get('interested', False)
        going = attrs.get('going', False)

        reactions_are_equal = interested == going
        if reactions_are_equal:
            raise serializers.ValidationError(_('Interested and going cannot be equal!'))

        return attrs


class EventSerializer(serializers.ModelSerializer):
    user_reactions = EventUserReactionSerializer(many=True, required=False)

    class Meta:
        model = models.Event
        fields = ('name', 'description', 'location', 'photo_urls', 'user_reactions')
        read_only_fields = ('photo_urls', )
