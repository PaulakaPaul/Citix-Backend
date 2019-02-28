from rest_framework import serializers

from apps.events import models


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = ('name', 'description', 'location', 'photo_urls')
