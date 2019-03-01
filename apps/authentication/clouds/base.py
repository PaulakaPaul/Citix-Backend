class BaseAuthClient:
    def create_user_with_email_and_password(self, email, password):
        raise NotImplementedError()

    def sign_in_with_email_and_password(self, email, password):
        raise NotImplementedError()


class BaseBucketClient:
    DEFAULT_IMAGE_EXTENSION = 'jpg'

    IMAGES_PATH = '/images/'
    IMAGES_EVENTS_PATH = IMAGES_PATH + 'events/'

    def add_cloud_photo_and_get_url(self, cloud_path, local_path, token):
        raise NotImplementedError()

    def create_event_cloud_path(self, event, file_extension):
        if not file_extension:
            file_extension = self.DEFAULT_IMAGE_EXTENSION

        return self.IMAGES_EVENTS_PATH + str(event.id) + '/' + str(len(event.photo_urls) - 1) + '.' + file_extension
