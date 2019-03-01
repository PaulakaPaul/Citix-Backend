import pyrebase
from django.conf import settings

from apps.authentication.clouds.base import BaseAuthClient, BaseBucketClient

config = {
    "apiKey": settings.FIREBASE_API_KEY,
    "authDomain": settings.FIREBASE_AUTH_DOMAIN,
    "databaseURL": settings.FIREBASE_DATABASE_URL,
    "storageBucket": settings.FIREBASE_STORAGE_BUCKET
}

firebase = pyrebase.initialize_app(config)


class FirebaseAuthClient(BaseAuthClient):
    auth = firebase.auth()

    def create_user_with_email_and_password(self, email, password):
        user = self.auth.create_user_with_email_and_password(email, password)

        return user

    def sign_in_with_email_and_password(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)

        return user


class FirebaseBucketClient(BaseBucketClient):
    bucket = firebase.storage()

    def add_cloud_photo_and_get_url(self, cloud_path, local_path, token):
        self.bucket.child(cloud_path).put(local_path, token)

        photo_url = self.bucket.child(cloud_path).get_url(token)

        return photo_url
