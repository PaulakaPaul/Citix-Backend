import pyrebase
from django.conf import settings

from apps.authentication.clouds.base import BaseAuthClient

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
        self.auth.create_user_with_email_and_password(email, password)
