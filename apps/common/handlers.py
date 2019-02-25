from rest_framework import exceptions
from rest_framework.views import exception_handler


def code_and_message_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, exceptions.APIException):
        response.data = exc.get_full_details()

    return response
