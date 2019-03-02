import tempfile

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from apps.authentication.clouds import get_bucket_cloud_client


class BaseAddPhotoView(APIView):
    """
        The model has to have a 'photo_urls' ArrayField() attribute to which the url it's appended.
    """

    model = None

    def post(self, request):
        assert self.model is not None

        user = request.user

        object_id_name = self._get_object_id_name()
        object_id = request.data.get(object_id_name, None)
        if object_id is None:
            raise ValidationError(_('{} is required.'.format(object_id_name)))

        try:
            obj = self.model.objects.get(id=object_id)
        except self.model.DoesNotExist:
            raise ValidationError(_('Requested {} does not exist.'.format(self._get_object_name())))

        files = request.FILES.getlist('photo_file')
        if len(files) != 1:
            raise ValidationError(_('Exactly one file has to be sent.'))

        requested_file = files[0]
        try:
            file_extension = requested_file.name.rsplit('.', 1)[1]
        except IndexError:
            file_extension = None

        bucket_cloud_client = get_bucket_cloud_client()
        cloud_object_path = bucket_cloud_client.create_object_cloud_path(obj, file_extension)

        with tempfile.NamedTemporaryFile() as file:
            # Write it in chunks for better memory performance.
            for chunk in requested_file.chunks():
                file.write(chunk)

            local_file_path = file.name
            token = user.auth_token.key
            url = bucket_cloud_client.add_cloud_photo_and_get_url(cloud_object_path, local_file_path, token)

            obj.photo_urls.append(url)
            obj.save()

            data = {
                "photo_url": url
            }

            return Response(data)

    def _get_object_id_name(self):
        return self._get_object_name() + '_id'

    def _get_object_name(self):
        return self.model.__name__.lower()
