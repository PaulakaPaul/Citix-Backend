class BaseAuthClient:
    def create_user_with_email_and_password(self, email, password):
        raise NotImplementedError()

    def sign_in_with_email_and_password(self, email, password):
        raise NotImplementedError()
