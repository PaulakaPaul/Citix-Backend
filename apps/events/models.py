from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4096)
    location = PointField()
    photo_urls = ArrayField(models.URLField())


class UserEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
