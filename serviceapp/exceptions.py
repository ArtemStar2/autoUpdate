from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response.status_code = 403  # Используйте 403 Forbidden вместо 401 Unauthorized

    return response