from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4096)
    location = PointField()
    photo_urls = ArrayField(models.URLField(max_length=2048), default=list)

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class EventUserReaction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='user_reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_reactions')

    interested = models.BooleanField(default=False)
    going = models.BooleanField(default=False)

    REACTIONS = ('interested', 'going', )

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        boolean_reactions = map(lambda reaction: getattr(self, reaction), self.REACTIONS)

        activated_reaction_index = list(boolean_reactions).index(True)
        activated_reaction = self.REACTIONS[activated_reaction_index]

        return activated_reaction.upper()
