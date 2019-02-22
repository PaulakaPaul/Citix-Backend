from apps.authentication.clouds.firebase import FirebaseAuthClient

auth_cloud_client = FirebaseAuthClient()


def get_auth_cloud_client():
    return auth_cloud_client
