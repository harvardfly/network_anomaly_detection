from rest_framework.views import exception_handler
from django.http.response import Http404


def rs_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['error'] = 1

    if isinstance(exc, Http404):
        response.data['detail'] = '404错误出现，请仔细检查。'

    return response
