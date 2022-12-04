import logging
import os

from django.http import JsonResponse
from django.http.response import HttpResponse
from requests import ConnectionError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # checks if the raised exception is of the type you want to handle
    if isinstance(exc, ConnectionError):
        # defines custom response data
        err_data = {'MSG_HEADER': 'some custom error messaging'}

        # logs detail data from the exception being handled
        logging.error(f"Original error detail and callstack: {exc}")
        # returns a JsonResponse
        return JsonResponse(err_data, safe=False, status=503)

    # returns response as handled normally by the framework
    if not bool(os.environ.get('DEBUG', False)):
        return HttpResponse("Not found")
    return response
