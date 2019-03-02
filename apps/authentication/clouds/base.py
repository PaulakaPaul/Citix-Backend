from apps.authentication.models import User
from apps.events.models import Event


class BaseAuthClient:
    def create_user_with_email_and_password(self, email, password):
        raise NotImplementedError()

    def sign_in_with_email_and_password(self, email, password):
        raise NotImplementedError()


class BaseBucketClient:
    DEFAULT_IMAGE_EXTENSION = 'jpg'

    IMAGES_PATH = '/images/'
    IMAGES_EVENTS_PATH = IMAGES_PATH + 'events/'
    IMAGES_USERS_PATH = IMAGES_PATH + 'users/'

    OBJECT_PATH_MAPPINGS = {
        Event: IMAGES_EVENTS_PATH,
        User: IMAGES_USERS_PATH
    }

    def add_cloud_photo_and_get_url(self, cloud_path, local_path, token):
        raise NotImplementedError()

    def create_object_cloud_path(self, obj, file_extension):
        """
            Functions works only for objects that have
            'photo_urls' ArrayField() attribute to calculate the path.
        """
        if not file_extension:
            file_extension = self.DEFAULT_IMAGE_EXTENSION

        return self._get_main_path(obj) + str(obj.id) + '/' + str(len(obj.photo_urls)) + '.' + file_extension

    def _get_main_path(self, obj):
        return self.OBJECT_PATH_MAPPINGS[obj.__class__]
