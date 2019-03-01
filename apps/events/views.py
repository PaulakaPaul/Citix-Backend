import tempfile

from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import gettext_lazy as _

from apps.authentication.clouds import get_bucket_cloud_client
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


class EventPhotoView(APIView):
    def post(self, request):
        user = request.user

        event_id = request.data.get('event_id', None)
        if event_id is None:
            raise ValidationError(_('event_id is required.'))

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise ValidationError(_('Requested event does not exist.'))

        files = request.FILES.getlist('photo_file')
        if len(files) != 1:
            raise ValidationError(_('Exactly one file has to be sent.'))

        requested_file = files[0]
        try:
            file_extension = requested_file.name.rsplit('.', 1)[1]
        except IndexError:
            file_extension = None

        bucket_cloud_client = get_bucket_cloud_client()
        cloud_event_path = bucket_cloud_client.create_event_cloud_path(event, file_extension)

        with tempfile.NamedTemporaryFile() as file:
            # Write it in chunks for better memory performance.
            for chunk in requested_file.chunks():
                file.write(chunk)

            file_name = file.name
            token = user.auth_token.key
            url = bucket_cloud_client.add_cloud_photo_and_get_url(cloud_event_path, file_name, token)

            event.photo_urls.append(url)
            event.save()

            data = {
                "photo_url": url
            }

            return Response(data)
